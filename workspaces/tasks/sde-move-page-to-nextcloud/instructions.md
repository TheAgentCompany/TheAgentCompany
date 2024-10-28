# **Instructions**

You will have to complete the two functions part of this project:

## **Task #1**

The first step is to implement a basic HyperLogLog data structure.

In `hyperloglog.h`, following functions have to be implemented:

* `HyperLogLog(inital_bits)`: a constructor where a number of leading bits (b) is provided.
* `GetCardinality()`: returns the cardinality value of a given set
* `AddElem(val)`: computes and places the value in the register.
* `ComputeCardinality()`: computes the cardinality based on the above formula.

Along with it, you can implement helper functions to implement the above (can add more as per requirement):

* `ComputeBinary(hash_t hash)`: It computes a binary of a given hash value. The hash value should be converted to a 64 bit binary stream (otherwise tests may fail).
* `PositionOfLeftmostOne(....)`: it computes the position of the leftmost 1.

For calculating hash, you can use the given function:

* `CalculateHash(...)` - to calculate hash

Please refer to the `std::bitset` library for storing in binary representation. When a value is obtained in decimal, convert into a greatest integer **less than or equal to** the decmial. Refer `std::floor` for more details.

## **Task #2**

In the second step, you will implement [Presto's](https://engineering.fb.com/2018/12/13/data-infrastructure/hyperloglog/) dense layout implementation of HLL (Refer to the dense layout section).

**Note:** In Presto's implementation, the binary rightmost contiguous set of zeros are counted (instead of the left zero count). In this task, similar approach should be used.

![HLL](https://15445.courses.cs.cmu.edu/fall2024/project0/img/presto.webp){width="400"}

The HLL stores overflow Buckets in the following manner: if the number of rightmost contiguous zeros are 33, its binary form will be `0100001`. In this scenario, it will be split into two pars, first 3 MSBs `010` and the last 4 LSBs `0001`. `0001` will be stored in the dense bucket, and the MSB `010` (which are overflowing bits) are stored in overflowing bucket.

In `hyperloglog_presto.h` following functions will be used for grading:

* `GetDenseBucket()` - Returns the dense bucket array
* `GetOverflowBucketOfIdx(..)` - Returns the overflow set of bits for the given index (if it exists).
* `GetCardinality()` - Returns the cardinality value

Do not delete the above functions.

Implement the following functions:

* `HyperLogLogPresto(initial_bits)` - a constructor for HyperLogLogPresto
* `AddElem()` - computes and places the value in the register.
* `ComputeCardinality()` - computes the cardinality based on the above formula.

For calculating hash, you can use the given function:

* `CalculateHash(...)` - to calculate hash

When a value is obtained in decimal, convert into a greatest integer **less than or equal to** the decmial.

## **Important Information**

* In **Task 2**, convert the hash value into 64-bit binary and then count the contiguous zeros (LSB).
* For calculating cardinality in both **Task 1** & **Task 2**, following steps should be followed.
  * Calculate the sum of the exponents and store it in memory using a `double` variable with default precision (no need for custom precision). The part of the formula to be stored in memory is shown below. Use `std::pow` for calculating the exponents.

  ![HLL](https://15445.courses.cs.cmu.edu/fall2024/project0/img/step1.png){width="300"}
  * Using the sum calculated above, determine the cardinality as shown below.

  ![HLL](https://15445.courses.cs.cmu.edu/fall2024/project0/img/step2.png){width="400"}
  * After obtaining the result above, convert it to the **greatest integer less than or equal to** the value. (as mentioned above).

Failing to follow the steps above may result in inaccurate outcomes that do not align with the test cases.

## **Setting Up Your Development Environment**

First install the packages that BusTub requires:

\# Linux $ sudo build_support/packages.sh # macOS $ build_support/packages.sh

See the README for additional information on how to setup different OS environments.

To build the system from the commandline, execute the following commands:

$ mkdir build $ cd build $ cmake -DCMAKE_BUILD_TYPE=Debug .. $ make -j\`nproc\`

We recommend always configuring CMake in debug mode. This will enable you to output debug messages and check for memory leaks (more on this in below sections).

## **Testing**

You can test the individual components of this assignment using our testing framework. We use [GTest](https://github.com/google/googletest) for unit test cases. You can disable tests in GTest by adding a `DISABLED_` prefix to the test name. To run the tests from the command-line:

$ cd build $ make -j$(nproc) hyperloglog_test $ ./test/hyperloglog_test