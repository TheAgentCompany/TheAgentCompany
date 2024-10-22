FROM base-image

# install libraries needed for evaluation
RUN pip install odfpy==1.4.1
RUN pip install pandas==2.0.0

ENV NEXTCLOUD_ADMIN_PASSWORD <YOUR_NEXTCLOUD_ADMIN_PASSWORD>

COPY salary.txt /utils

