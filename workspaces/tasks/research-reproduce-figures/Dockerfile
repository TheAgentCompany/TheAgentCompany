FROM ghcr.io/li-boxuan/task-base-image:1.0.0

RUN apt-get update && apt-get install -y poppler-utils

COPY eval_data/* /utils

RUN pip install pdf2image==1.17.0