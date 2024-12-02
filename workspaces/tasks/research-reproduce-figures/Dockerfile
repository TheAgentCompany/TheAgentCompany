FROM base-image

RUN apt-get update && apt-get install -y poppler-utils

RUN mkdir -p /eval_data

COPY eval_data/* /eval_data

RUN pip install pdf2image=1.17.0