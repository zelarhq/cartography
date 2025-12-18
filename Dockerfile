# Base image
FROM python:3.10.19-slim@sha256:fb1feae978f1729094eb0405e5f9564e55b2b3b24db3261d30ba4f22c5001a8a AS base
# Default to ''. Overridden with a specific version specifier e.g. '==0.98.0' by build args or from GitHub actions.
ARG VERSION_SPECIFIER
# the UID and GID to run cartography as
# (https://github.com/hexops/dockerfile#do-not-use-a-uid-below-10000).
ARG uid=10001
ARG gid=10001
USER ${uid}:${gid}
WORKDIR /var/cartography
ENV HOME=/var/cartography



# Intermediate image to build the venv
FROM base AS builder
# Re-declare build args in this stage (Docker requires this per-stage).
ARG VERSION_SPECIFIER
ARG uid=10001
ARG gid=10001

# Install build-time OS deps needed when installing from source (setuptools-scm needs `git`).
USER root
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Back to the non-root runtime user.
USER ${uid}:${gid}

# Install uv version 0.7.3
COPY --from=ghcr.io/astral-sh/uv@sha256:87a04222b228501907f487b338ca6fc1514a93369bfce6930eb06c8d576e58a4 /uv /uvx /bin/
# Install cartography
#
# Why: `uv tool install cartography${VERSION_SPECIFIER}` installs from PyPI. If VERSION_SPECIFIER is unset/empty,
# the resulting image content changes over time and may not include recently-added CLI flags (e.g. `--konnect-*`).
# Installing from the checked-out source tree (this repo) makes the image deterministic and keeps CLI args in sync
# with the code you are building.
COPY --chown=${uid}:${gid} . /src
RUN ls -alh /var/cartography
RUN if [ -n "${VERSION_SPECIFIER}" ]; then \
        uv tool install "cartography${VERSION_SPECIFIER}"; \
    else \
        uv tool install /src; \
    fi
RUN ls -alh /var/cartography


# Final production image
FROM base AS production
# Copy venv from the builder stage
COPY --from=builder --chown=${uid}:${gid} /var/cartography/.local /var/cartography/.local
ENV PATH="/var/cartography/.local/bin:$PATH"
# verify that the binary at least runs
RUN cartography -h

ENTRYPOINT ["cartography"]
CMD ["-h"]
