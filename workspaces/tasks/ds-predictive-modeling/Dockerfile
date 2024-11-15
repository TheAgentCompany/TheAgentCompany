FROM base-image

RUN pip install pandas==2.2.3
RUN pip install scikit-learn==1.5.2
RUN pip install numpy==2.1.2

COPY stock_train_raw.csv /workspace
COPY stock_test.csv /workspace

COPY golden_answer.csv /utils