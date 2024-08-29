# do initialization
sh update_hosts.sh
python functionality.py

# sleep and run evaluactor
sleep 10 && python evaluator.py

# keep container running
tail -f /dev/null