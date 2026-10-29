FROM --platform=linux/amd64 alpine:3.22 AS download

ARG MINIO_RELEASE=RELEASE.2024-11-07T00-52-20Z
ARG MINIO_SHA256=c27873d791b56d33518de11f12c5bfae4be88ebac00e12c6dd0027b08123fd80

RUN apk add --no-cache ca-certificates curl \
    && curl --fail --location --silent --show-error \
        "https://github.com/minio/minio/releases/download/${MINIO_RELEASE}/minio.linux-amd64.${MINIO_RELEASE}" \
        --output /tmp/minio \
    && echo "${MINIO_SHA256}  /tmp/minio" | sha256sum -c - \
    && install -D -m 0755 /tmp/minio /usr/local/bin/minio

FROM --platform=linux/amd64 alpine:3.22

COPY --from=download /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=download /usr/local/bin/minio /usr/local/bin/minio

EXPOSE 9000 9090
VOLUME ["/export"]

ENTRYPOINT ["/usr/local/bin/minio"]
CMD ["server", "/export", "--console-address", ":9090"]
