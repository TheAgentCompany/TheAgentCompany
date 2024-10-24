FROM base-image

# persist utilities files in the exam image
COPY evaluator.py /utils/
COPY init.sh /utils/
RUN chmod +x /utils/init.sh

# persist instruction files needed by the examinee
COPY task.md /instruction/

# requests library is needed for this task's evaluation
# this is optional and benchmark developers should customize according
# to their tasks' needs
RUN pip install requests
