import logging
from typing import List
from scoring import Result, Checkpoint
from common import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.protocol import GremlinServerError

# Check if JanusGraph repo is cloned
@grader
def grade_checkpoint1():
    return check_repo_exists('janusgraph')

# Check if JanusGraph Server is running via WebSocket
@grader
def grade_checkpoint2():
    # Build the connection
    conn = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
    g = traversal().withRemote(conn)
    
    count = g.V().count().next()
    conn.close()
    return True
    

# Check if the graph structure matches the expected hierarchy
@grader
def grade_checkpoint3():
    conn = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
    g = traversal().withRemote(conn)
    
    # Verify Sarah Johnson as CTO
    sarah = g.V().has('person', 'name', 'Sarah Johnson').has('title', 'CTO').count().next()
    if sarah != 1:
        return False
        
    # Verify direct reports to Sarah
    direct_reports = g.V().has('name', 'Sarah Johnson').in_('reports_to').count().next()
    if direct_reports != 4: 
        return False
        
    # Check Mike Chen's team
    mike_reports = g.V().has('name', 'Mike Chen').in_('reports_to').count().next()
    if mike_reports != 2:  
        return False
        
    # Check Zhang Wei's team
    zhang_reports = g.V().has('name', 'Zhang Wei').in_('reports_to').count().next()
    if zhang_reports != 1:  
        return False
        
    # Verify titles
    titles = {
        'Mike Chen': 'Senior Software Engineer',
        'Zhang Wei': 'Senior Software Engineer',
        'Wang Fang': 'AI Researcher',
        'Li Ming': 'Database Project Manager',
        'Emily Zhou': 'Software Engineer',
        'Emma Lewis': 'Software Engineer',
        'Alex Turner': 'Software Engineer'
    }
    
    for name, title in titles.items():
        count = g.V().has('name', name).has('title', title).count().next()
        if count != 1:
            return False
    
    conn.close()
    return True
        
    

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    
    checkpoint1_passed = grade_checkpoint1()
    checkpoint2_passed = grade_checkpoint2()
    checkpoint3_passed = grade_checkpoint3()
    
    checkpoints.append(Checkpoint(1, int(checkpoint1_passed)))
    checkpoints.append(Checkpoint(1, int(checkpoint2_passed)))
    checkpoints.append(Checkpoint(2, int(checkpoint3_passed) * 2))
    
    return result