Find copilot arena's api server codebase in our gitlab (located at http://the-agent-company.com:8929/root/copilot-arena-server)
Pull this repository down to /workspace folder and then install the requirements.txt
Edit the create_pair endpoint so that it now requires the suffix key as an input
At the end, start the server in the background. To start the server, run the command:
uvicorn app:app --host 0.0.0.0 --port 5000 --workers 1 --log-config log_conf.yaml&