# do initialization
sh initialization.sh
python initialization.py

# sleep and run evaluactor
sleep 10 && python evaluator.py

# keep container running
tail -f /dev/null