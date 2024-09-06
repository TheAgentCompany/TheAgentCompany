FROM base-image

COPY evaluator.py /evaluation/

COPY task.md /instruction/

# requests library is needed for evaluation
RUN pip install requests

# initialization code
RUN sh run.sh


