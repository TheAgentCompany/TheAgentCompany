To retrieve a filtered list of issues with their brief details, you'll need to locate the appropriate API endpoint at http://the-agent-company.com:8091/.
Specifically, you want to fetch the 10 most recent issues from the 'tac' workspace, ordered by due date. To accomplish this:
Monitor the network requests to identify the correct API endpoint
Note the required parameters (using cursor value 10:0:0)
Save the complete URL including all GET parameters to /workspace/url_for_issues.txt