FROM python:3

# create evaluation directory (examinee MUST not access this directory)
RUN mkdir -p /evaluation

# create and set up working directory
RUN mkdir -p /workspace
WORKDIR /workspace

COPY test_setup.py /evaluation/