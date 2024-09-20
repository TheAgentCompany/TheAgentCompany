FROM base-image

# persist utilities files in the exam image
COPY evaluator.py /utils/
COPY init.sh /utils/
RUN chmod +x /utils/init.sh
COPY pre_init.py /utils/
COPY post_init.py /utils/

# persist instruction files needed by the examinee
COPY task.md /instruction/

# download the reference image and ensure it exists
RUN set -e && \
    curl -f -S -v -o /utils/reference.jpg https://images.pexels.com/photos/27220813/pexels-photo-27220813.jpeg && \
    [ -s /utils/reference.jpg ] || (echo "Failed to download image" && exit 1)

# numpy library is needed for this task's evaluation
RUN pip install numpy

# requests library is needed for this task's sanity checks
RUN pip install requests
