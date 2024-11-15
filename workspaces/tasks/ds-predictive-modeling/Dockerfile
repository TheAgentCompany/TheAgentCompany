FROM base-image

RUN pip install pandas==1.0.3
RUN pip install sklearn==1.5.2
RUN pip install numpy==2.1.2

COPY stock_train_raw.csv /workspace
COPY stock_test.csv /workspace

COPY golden_answer.csv /utils