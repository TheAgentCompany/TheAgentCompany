The repository is located in workspace/copilot-arena-server.
Create a new POST endpoint to the server called mock_create_pair.
It should return the same JSON as create_pair, except with a "test" as both the completions,
rather than actually calling any APIs.
At the end, start the server. To start the server, run the command:
uvicorn app:app --host 0.0.0.0 --port 5000 --workers 1 --log-config log_conf.yaml