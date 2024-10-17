FROM base-image

# download the reference image and ensure it exists
RUN set -e && \
    curl -f -S -v -o /utils/reference.jpg https://images.pexels.com/photos/27220813/pexels-photo-27220813.jpeg && \
    [ -s /utils/reference.jpg ] || (echo "Failed to download image" && exit 1)

# numpy library is needed for this task's evaluation
RUN pip install numpy
