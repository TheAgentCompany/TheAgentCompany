Find copilot arena's api server codebase in our gitlab (located at http://the-agent-company.com:8929/root/copilot-arena-server)
Clone the server repository to the /workspace folder and start up the API server locally.
Make sure to install the correct requirements by running `pip install -r requirements.txt`
Create a new POST endpoint to the server called mock_create_pair.
It should return the same JSON as create_pair, except with a "test" as both the completions,
rather than actually calling any APIs.
At the end, start the server in the background. To start the server, run the command:
uvicorn app:app --host 0.0.0.0 --port 5000 --workers 1 --log-config log_conf.yaml