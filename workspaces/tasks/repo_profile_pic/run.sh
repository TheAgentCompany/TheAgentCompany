# do initialization
curl -o reference.jpg https://images.pexels.com/photos/27220813/pexels-photo-27220813.jpeg?cs=srgb&dl=pexels-nati-87264186-27220813.jpg&fm=jpg
python functionality.py

# sleep and run evaluactor
sleep 10 && python evaluator.py

# keep container running
tail -f /dev/null