# Local MinIO image for Plane

The Plane deployment pins `minio/minio:RELEASE.2024-11-07T00-52-20Z`, but that tag currently cannot be pulled from Docker Hub. This local image packages the official MinIO Linux AMD64 binary from the exact same release; it does not substitute a MinIO release or change Plane's object-storage format.

Build it locally under the distinct image name used by the deployment Compose file:

```sh
docker build \
  -t tac-minio:RELEASE.2024-11-07T00-52-20Z \
  -f servers/plane/minio/Dockerfile \
  servers/plane/minio
```

Then start Plane with the existing compose files. Its MinIO service uses the same `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` environment variables, runs `server /export --console-address ":9090"`, and mounts the existing `uploads` volume at `/export`. The local image declares that same command, entrypoint, ports, and data path. MinIO reads the root credentials directly from its environment; no wrapper script is needed. The Dockerfile's entrypoint invokes the binary directly, equivalent to the official image entrypoint prepending `minio` to the Compose command.

## Release identity and verification

- Release: `RELEASE.2024-11-07T00-52-20Z`
- Asset: [`minio.linux-amd64.RELEASE.2024-11-07T00-52-20Z`](https://github.com/minio/minio/releases/download/RELEASE.2024-11-07T00-52-20Z/minio.linux-amd64.RELEASE.2024-11-07T00-52-20Z)
- Asset size: 103,751,832 bytes
- SHA-256: `c27873d791b56d33518de11f12c5bfae4be88ebac00e12c6dd0027b08123fd80`

The checksum matches both the official release `.sha256sum` asset and the GitHub release API's digest for the binary asset. The build checks this value before copying the executable into the runtime stage. This recipe targets Linux AMD64, matching the inspected release asset.

The official [release Dockerfile](https://github.com/minio/minio/blob/RELEASE.2024-11-07T00-52-20Z/Dockerfile.release) installs the MinIO executable and configures an entrypoint that prepends `minio` when Compose passes `server ...`. The official [entrypoint](https://github.com/minio/minio/blob/RELEASE.2024-11-07T00-52-20Z/dockerscripts/docker-entrypoint.sh) performs only that argument normalization before executing the binary. This image expresses the same startup directly as `ENTRYPOINT ["/usr/local/bin/minio"]` and the server command as `CMD`.
