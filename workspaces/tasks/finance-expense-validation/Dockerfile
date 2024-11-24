FROM base-image

# install libraries needed for evaluation
RUN pip install pandas==2.2.3
RUN pip install openpyxl==3.1.5

COPY ref_expenses_analysis.csv /utils
COPY ref_expenses_corrected.xlsx /utils
