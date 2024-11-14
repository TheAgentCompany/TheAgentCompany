FROM base-image

RUN pip install pandas==2.2.3
RUN pip install PyPDF2==3.0.1

COPY personell_data_golden.csv /utils
COPY TAC_personell_data.csv /workspace
COPY i-9.pdf /workspace