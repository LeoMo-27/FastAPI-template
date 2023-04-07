# Environment setter image
FROM python:3.10-buster AS environment

ARG DEV=false

# Set up environmental variables
ENV LANG=C.UTF-8 \
    # python:
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.4.1

# Set up workdir for environment
WORKDIR /app

# Install OS package dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    apt-get purge && \
    rm -rf /var/lib/apt/lists/* /tmp/* && \
    # Install poetry
    pip install "poetry==$POETRY_VERSION"

# Setup the virtualenv
RUN python -m venv /.venv

# Copy Makefile
COPY Makefile ./Makefile

# Copy project dependency files to image
COPY pyproject.toml poetry.lock ./

# Activate virtualenv and install dependencies
RUN . /.venv/bin/activate && \
    if $DEV; then make build-dev; else make build; fi

# --------------------------------------------------------

# Final image
FROM python:3.10-slim-buster AS final

# Set up environmental variables
ENV LANG=C.UTF-8

# Set up base workdir
WORKDIR /app

# Get virtual environment
COPY --from=environment /.venv /.venv

# Use executables from the virtual env
ENV PATH="/.venv/bin:$PATH"

# Copy files to image
COPY . .
