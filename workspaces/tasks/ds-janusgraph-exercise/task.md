Your task is to implement a company's organizational chart using JanusGraph graph database.

1. Clone JanusGraph repository (http://the-agent-company.com:8929/root/janusgraph) under /workspace folder

2. Launch JanusGraph server and ensure it's running on port 8182 with websocket mode

3. Create an organization structure in JanusGraph that matches exactly with the hierarchy shown in employee_diagram.jpg (provided under /workspace folder)

You need to:
1. Create vertices for each employee with properties:
   - label: 'person'
   - name: employee's full name
   - title: employee's job title

2. Create edges between employees to represent reporting relationships:
   - edge label: 'reports_to'
   - direction: from subordinate to manager

The graph must match the exact structure and relationships shown in employee_diagram.jpg.