FROM python:3

# create evaluation directory (examinee MUST not access this directory)
RUN mkdir -p /evaluation

# create instruction directory (examinee should read instructions from here)
RUN mkdir -p /instruction
COPY test_setup.py /instruction

# create and set up working directory
RUN mkdir -p /workspace
WORKDIR /workspace
