FROM python:3.10.13-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR app/

FROM base AS builder

COPY ./src ./src
COPY ./pyproject.toml ./

RUN pip install build && \
    python3 -m build --wheel

FROM base AS production

COPY --from=builder ./app/dist ./

RUN pip install marketplace*.whl

CMD ["bot"]
