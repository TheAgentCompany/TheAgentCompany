package raft

//
// Raft tests.
//
// we will use the original test_test.go to test your code for grading.
// so, while you can modify this code to help you debug, please
// test with the original before submitting.
//

import "testing"
import "fmt"
import "time"
import "math/rand"
import "sync"

// The tester generously allows solutions to complete elections in one second
// (much more than the paper's range of timeouts).
const RaftElectionTimeout = 1000 * time.Millisecond

func TestInitialElection3A(t *testing.T) {
	servers := 3
	cfg := make_config(t, servers, false)
	defer cfg.cleanup()

	fmt.Printf("Test (3A): initial election ...\n")

	// is a leader elected?
	cfg.checkOneLeader()

	// does the leader+term stay the same if there is no network failure?
	term1 := cfg.checkTerms()
	time.Sleep(2 * RaftElectionTimeout)
	term2 := cfg.checkTerms()
	if term1 != term2 {
		fmt.Printf("warning: term changed even though there were no failures")
	}

	fmt.Printf("  ... Passed\n")
}

func TestReElection3A(t *testing.T) {
	servers := 3
	cfg := make_config(t, servers, false)
	defer cfg.cleanup()

	fmt.Printf("Test (3A): election after network failure ...\n")
	fmt.Printf("Basic 1 leader\n")
	leader1 := cfg.checkOneLeader()

	// if the leader disconnects, a new one should be elected.
	fmt.Printf("1 disconnected leader\n")
	cfg.disconnect(leader1)
	cfg.checkOneLeader()

	// if the old leader rejoins, that shouldn't
	// disturb the old leader.
	fmt.Printf("old connected 1 leader\n")
	cfg.connect(leader1)
	leader2 := cfg.checkOneLeader()

	// if there's no quorum, no leader should
	// be elected.
	fmt.Printf("2 disconnected no leader\n")
	cfg.disconnect(leader2)
	cfg.disconnect((leader2 + 1) % servers)
	time.Sleep(2 * RaftElectionTimeout)
	cfg.checkNoLeader()

	fmt.Printf(" reconnected 1 leader\n")
	// if a quorum arises, it should elect a leader.
	cfg.connect((leader2 + 1) % servers)
	cfg.checkOneLeader()

	// re-join of last node shouldn't prevent leader from existing.
	fmt.Printf("1 reconnected 1 leader\n")
	cfg.connect(leader2)
	cfg.checkOneLeader()

	fmt.Printf("  ... Passed\n")
}

func TestBasicAgree3B(t *testing.T) {
	servers := 5
	cfg := make_config(t, servers, false)
	defer cfg.cleanup()

	fmt.Printf("Test (3B): basic agreement ...\n")
	DPrintf("\nTest (3B): basic agreement ...\n")

	iters := 3
	for index := 1; index < iters+1; index++ {
		nd, _ := cfg.nCommitted(index)
		if nd > 0 {
			t.Fatalf("some have committed before Start()")
		}

		// fmt.Printf("Starting for %d\n", index)

		xindex := cfg.one(index*100, servers)
		//fmt.Printf("Index returned %d\n", xindex)
		if xindex != index {
			t.Fatalf("got index %v but expected %v", xindex, index)
		}
	}

	fmt.Printf("  ... Passed\n")
}

func TestFailAgree3B(t *testing.T) {
	servers := 3
	cfg := make_config(t, servers, false)
	defer cfg.cleanup()

	fmt.Printf("Test (3B): agreement despite follower disconnection ...\n")
	DPrintf("\nTest (3B): agreement despite follower disconnection ...\n")

	cfg.one(101, servers)

	// follower network disconnection
	fmt.Printf("\nCHecking one leader\n")
	DPrintf("\nCHecking one leader\n")
	leader := cfg.checkOneLeader()
	cfg.disconnect((leader + 1) % servers)

	fmt.Printf("\nCHecking agreement with one disconnected server\n")
	DPrintf("\nCHecking agreement with one disconnected server\n")
	// agree despite one disconnected server?
	cfg.one(102, servers-1)
	cfg.one(103, servers-1)
	time.Sleep(RaftElectionTimeout)
	cfg.one(104, servers-1)
	cfg.one(105, servers-1)

	// re-connect
	cfg.connect((leader + 1) % servers)
	fmt.Printf("\nCHecking with reconnected server\n")
	DPrintf("\nCHecking with reconnected server\n")
	// agree with full set of servers?
	cfg.one(106, servers)
	time.Sleep(RaftElectionTimeout)
	cfg.one(107, servers)

	fmt.Printf("  ... Passed\n")
}

func TestFailNoAgree3B(t *testing.T) {
	servers := 5
	cfg := make_config(t, servers, false)
	defer cfg.cleanup()

	fmt.Printf("Test (3B): no agreement if too many followers disconnect ...\n")
	DPrintf("\nTest (3B): no agreement if too many followers disconnect ...\n")

	cfg.one(10, servers)

	// 3 of 5 followers disconnect
	fmt.Println("\n3 of 5 followers disconnect")
	leader := cfg.checkOneLeader()
	DPrintf("\n3 of 5 followers disconnect %d, %d, %d.\n", (leader+1)%servers, (leader+2)%servers, (leader+3)%servers)
	cfg.disconnect((leader + 1) % servers)
	cfg.disconnect((leader + 2) % servers)
	cfg.disconnect((leader + 3) % servers)

	index, _, ok := cfg.rafts[leader].Start(20)
	if ok != true {
		t.Fatalf("leader rejected Start()")
	}
	if index != 2 {
		t.Fatalf("expected index 2, got %v", index)
	}

	time.Sleep(2 * RaftElectionTimeout)

	n, _ := cfg.nCommitted(index)
	if n > 0 {
		t.Fatalf("%v committed but no majority", n)
	}

	// repair
	fmt.Println("\nrepair.")
	DPrintf("\nrepair.")
	cfg.connect((leader + 1) % servers)
	cfg.connect((leader + 2) % servers)
	cfg.connect((leader + 3) % servers)

	// the disconnected majority may have chosen a leader from
	// among their own ranks, forgetting index 2.
	// or perhaps
	leader2 := cfg.checkOneLeader()
	index2, _, ok2 := cfg.rafts[leader2].Start(30)
	if ok2 == false {
		t.Fatalf("leader2 rejected Start()")
	}
	if index2 < 2 || index2 > 3 {
		t.Fatalf("unexpected index %v", index2)
	}

	cfg.one(1000, servers)

	fmt.Printf("  ... Passed\n")
}

func TestConcurrentStarts3B(t *testing.T) {
	servers := 3
	cfg := make_config(t, servers, false)
	defer cfg.cleanup()

	fmt.Printf("Test (3B): concurrent Start()s ...\n")
	DPrintf("\nTest (3B): concurrent Start()s ...\n")

	var success bool
loop:
	for try := 0; try < 5; try++ {
		if try > 0 {
			// give solution some time to settle
			time.Sleep(3 * time.Second)
		}

		leader := cfg.checkOneLeader()
		_, term, ok := cfg.rafts[leader].Start(1)

		if !ok {
			// leader moved on really quickly
			continue
		}

		iters := 5
		var wg sync.WaitGroup
		is := make(chan int, iters)
		for ii := 0; ii < iters; ii++ {
			wg.Add(1)
			go func(i int) {
				defer wg.Done()
				i, term1, ok := cfg.rafts[leader].Start(100 + i)
				if term1 != term {
					return
				}
				if ok != true {
					return
				}
				is <- i
			}(ii)
		}

		wg.Wait()
		close(is)

		for j := 0; j < servers; j++ {
			if t, _ := cfg.rafts[j].GetState(); t != term {
				// term changed -- can't expect low RPC counts
				continue loop
			}
		}

		failed := false
		cmds := []int{}
		for index := range is {
			cmd := cfg.wait(index, servers, term)
			if ix, ok := cmd.(int); ok {
				if ix == -1 {
					// peers have moved on to later terms
					// so we can't expect all Start()s to
					// have succeeded
					failed = true
					break
				}
				cmds = append(cmds, ix)
			} else {
				t.Fatalf("value %v is not an int", cmd)
			}
		}

		if failed {
			// avoid leaking goroutines
			go func() {
				for range is {
				}
			}()
			continue
		}

		for ii := 0; ii < iters; ii++ {
			x := 100 + ii
			ok := false
			for j := 0; j < len(cmds); j++ {
				if cmds[j] == x {
					ok = true
				}
			}
			if ok == false {
				t.Fatalf("cmd %v missing in %v", x, cmds)
			}
		}

		success = true
		break
	}

	if !success {
		t.Fatalf("term changed too often")
	}

	fmt.Printf("  ... Passed\n")
}

func TestRejoin3B(t *testing.T) {
	servers := 3
	cfg := make_config(t, servers, false)
	defer cfg.cleanup()

	fmt.Printf("Test (3B): rejoin of partitioned leader ...\n")
	DPrintf("\nTest (3B): rejoin of partitioned leader ...\n")

	cfg.one(101, servers)

	// leader network failure
	leader1 := cfg.checkOneLeader()
	cfg.disconnect(leader1)

	// make old leader try to agree on some entries
	cfg.rafts[leader1].Start(102)
	cfg.rafts[leader1].Start(103)
	cfg.rafts[leader1].Start(104)

	// new leader commits, also for index=2
	cfg.one(103, 2)

	// new leader network failure
	leader2 := cfg.checkOneLeader()
	cfg.disconnect(leader2)

	// old leader connected again
	cfg.connect(leader1)

	cfg.one(104, 2)

	// all together now
	cfg.connect(leader2)

	cfg.one(105, servers)

	fmt.Printf("  ... Passed\n")
}

func TestBackup3B(t *testing.T) {
	servers := 5
	cfg := make_config(t, servers, false)
	defer cfg.cleanup()

	fmt.Printf("Test (3B): leader backs up quickly over incorrect follower logs ...\n")
	DPrintf("\nTest (3B): leader backs up quickly over incorrect follower logs ...\n")

	cfg.one(rand.Int(), servers)

	// put leader and one follower in a partition

	leader1 := cfg.checkOneLeader()
	DPrintf("\nput leader and one follower in a partition. Current leader: %d, disconnected server: %d %d %d\n",
		leader1, (leader1+2)%servers, (leader1+3)%servers, (leader1+4)%servers)
	fmt.Printf("\nput leader and one follower in a partition. Current leader: %d, disconnected server: %d %d %d\n",
		leader1, (leader1+2)%servers, (leader1+3)%servers, (leader1+4)%servers)
	cfg.disconnect((leader1 + 2) % servers)
	cfg.disconnect((leader1 + 3) % servers)
	cfg.disconnect((leader1 + 4) % servers)

	// submit lots of commands that won't commit
	DPrintf("\nsubmit lots of commands that won't commit.\n")
	fmt.Printf("\nsubmit lots of commands that won't commit.\n")
	for i := 0; i < 20; i++ {
		//	for i := 0; i < 50; i++ {
		cfg.rafts[leader1].Start(rand.Int())
	}

	time.Sleep(RaftElectionTimeout / 2)

	cfg.disconnect((leader1 + 0) % servers)
	cfg.disconnect((leader1 + 1) % servers)

	// allow other partition to recover
	DPrintf("\nallow other partition to recover. Server %d %d %d come back.\n", (leader1+2)%servers, (leader1+3)%servers, (leader1+4)%servers)
	fmt.Printf("\nallow other partition to recover. Server %d %d %d come back.\n", (leader1+2)%servers, (leader1+3)%servers, (leader1+4)%servers)
	cfg.connect((leader1 + 2) % servers)
	cfg.connect((leader1 + 3) % servers)
	cfg.connect((leader1 + 4) % servers)

	leader3 := cfg.checkOneLeader()

	// lots of successful commands to new group.
	DPrintf("\ncurrent leader: %d, lots of successful commands to new group.\n", leader3)
	fmt.Printf("\ncurrent leader: %d, lots of successful commands to new group.\n", leader3)
	for i := 0; i < 20; i++ {
		//	for i := 0; i < 50; i++ {
		cfg.one(rand.Int(), 3)
	}

	// now another partitioned leader and one follower
	DPrintf("\nnow another partitioned leader and one follower.\n")
	fmt.Printf("\nnow another partitioned leader and one follower.\n")
	leader2 := cfg.checkOneLeader()
	other := (leader1 + 2) % servers
	if leader2 == other {
		other = (leader2 + 1) % servers
	}
	DPrintf("\nDisconnected %d, current leader %d.\n", other, leader2)
	fmt.Printf("\nDisconnected %d, current leader %d.\n", other, leader2)
	cfg.disconnect(other)

	// lots more commands that won't commit
	DPrintf("\ncurrent leader: %d, lots more commands that won't commit\n", leader2)
	fmt.Printf("\ncurrent leader: %d, lots more commands that won't commit\n", leader2)
	for i := 0; i < 20; i++ {
		//	for i := 0; i < 50; i++ {
		cfg.rafts[leader2].Start(rand.Int())
	}

	time.Sleep(RaftElectionTimeout / 2)

	// bring original leader back to life,
	DPrintf("\n")
	fmt.Println()
	for i := 0; i < servers; i++ {
		cfg.disconnect(i)
		DPrintf("raft %d disconnected.\n", i)
		fmt.Printf("raft %d disconnected.\n", i)
	}
	fmt.Printf("\nbring original leader back to life. Server %d %d %d.\n", (leader1+0)%servers, (leader1+1)%servers, other)
	DPrintf("\nbring original leader back to life. Server %d %d %d.\n", (leader1+0)%servers, (leader1+1)%servers, other)
	cfg.connect((leader1 + 0) % servers)
	cfg.connect((leader1 + 1) % servers)
	cfg.connect(other)

	//	leader4 := cfg.checkOneLeader()
	//	DPrintf("current leader: %d.\n", leader4)
	//	fmt.Printf("current leader: %d.\n", leader4)

	// lots of successful commands to new group.
	DPrintf("\nlots of successful commands to new group.\n")
	fmt.Printf("\nlots of successful commands to new group.\n")
	for i := 0; i < 20; i++ {
		//	for i := 0; i < 50; i++ {
		cfg.one(rand.Int(), 3)
	}

	// now everyone
	DPrintf("\nnow everyone\n")
	fmt.Printf("\nnow everyone\n")
	for i := 0; i < servers; i++ {
		cfg.connect(i)
	}
	cfg.one(rand.Int(), servers)

	fmt.Printf("  ... Passed\n")
}

func TestCount3B(t *testing.T) {
	servers := 3
	cfg := make_config(t, servers, false)
	defer cfg.cleanup()

	fmt.Printf("Test (3B): RPC counts aren't too high ...\n")
	DPrintf("\nTest (3B): RPC counts aren't too high ...\n")

	rpcs := func() (n int) {
		for j := 0; j < servers; j++ {
			n += cfg.rpcCount(j)
		}
		return
	}

	leader := cfg.checkOneLeader()

	total1 := rpcs()

	if total1 > 30 || total1 < 1 {
		t.Fatalf("too many or few RPCs (%v) to elect initial leader\n", total1)
	}

	var total2 int
	var success bool
loop:
	for try := 0; try < 5; try++ {
		if try > 0 {
			// give solution some time to settle
			time.Sleep(3 * time.Second)
		}

		leader = cfg.checkOneLeader()
		total1 = rpcs()

		iters := 10
		starti, term, ok := cfg.rafts[leader].Start(1)
		if !ok {
			// leader moved on really quickly
			continue
		}
		cmds := []int{}
		for i := 1; i < iters+2; i++ {
			x := int(rand.Int31())
			cmds = append(cmds, x)
			index1, term1, ok := cfg.rafts[leader].Start(x)
			if term1 != term {
				// Term changed while starting
				continue loop
			}
			if !ok {
				// No longer the leader, so term has changed
				continue loop
			}
			if starti+i != index1 {
				t.Fatalf("Start() failed")
			}
		}

		for i := 1; i < iters+1; i++ {
			cmd := cfg.wait(starti+i, servers, term)
			if ix, ok := cmd.(int); ok == false || ix != cmds[i-1] {
				if ix == -1 {
					// term changed -- try again
					continue loop
				}
				t.Fatalf("wrong value %v committed for index %v; expected %v\n", cmd, starti+i, cmds)
			}
		}

		failed := false
		total2 = 0
		for j := 0; j < servers; j++ {
			if t, _ := cfg.rafts[j].GetState(); t != term {
				// term changed -- can't expect low RPC counts
				// need to keep going to update total2
				failed = true
			}
			total2 += cfg.rpcCount(j)
		}

		if failed {
			continue loop
		}

		if total2-total1 > (iters+1+3)*3 {
			t.Fatalf("too many RPCs (%v) for %v entries, expected %d\n", total2-total1, iters, (iters+1+3)*3)
		}

		success = true
		break
	}

	if !success {
		t.Fatalf("term changed too often")
	}

	time.Sleep(RaftElectionTimeout)

	total3 := 0
	for j := 0; j < servers; j++ {
		total3 += cfg.rpcCount(j)
	}

	if total3-total2 > 3*20 {
		t.Fatalf("too many RPCs (%v) for 1 second of idleness\n", total3-total2)
	}

	fmt.Printf("  ... Passed\n")
}