FROM base-image

# persist utilities files in the exam image
COPY evaluator.py /utils/
COPY init.sh /utils/
RUN chmod +x /utils/init.sh
COPY pre_init.py /utils/
COPY post_init.py /utils/
COPY populate_data.py /utils/

# persist instruction files needed by the examinee
COPY task.md /instruction/

# install libraries needed for evaluation
RUN pip install requests
RUN pip install beautifulsoup4
RUN pip install xml.etree.ElementTree
