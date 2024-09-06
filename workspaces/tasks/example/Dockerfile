FROM base-image

# persist evaluator and task files in the exam image
COPY evaluator.py /evaluation/
COPY task.md /instruction/

# requests library is needed for evaluation (optional)
RUN pip install requests

# copy and run initialization code (optional)
COPY init.sh /
COPY init.py /
RUN chmod +x /init.sh
RUN sh /init.sh
RUN python /init.py

# keep the container running (optional)
CMD ["tail", "-f","/dev/null"]