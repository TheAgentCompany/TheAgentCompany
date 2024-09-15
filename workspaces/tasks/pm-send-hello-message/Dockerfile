FROM base-image

# persist utilities files in the exam image
COPY evaluator.py /utils/
COPY init.sh /utils/
RUN chmod +x /utils/init.sh
COPY pre_init.py /utils/
COPY post_init.py /utils/

# persist instruction files needed by the examinee
COPY task.md /instruction/

# requests library is needed for evaluation
RUN pip install requests