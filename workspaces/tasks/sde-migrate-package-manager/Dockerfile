FROM ghcr.io/li-boxuan/task-base-image:1.0.0

# Install both poetry and uv for migration
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && curl -LsSf https://astral.sh/uv/install.sh | sh