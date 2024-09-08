FROM python:3.12-slim as base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    curl
RUN cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone
ENV PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_HOME=$HOME/.poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    WORKDIR=/code
ENV PATH="$POETRY_HOME/bin:$PATH" \
    TALIB_PREFIX=/opt/talib_c
ENV TA_LIBRARY_PATH=$TALIB_PREFIX/lib \
    TA_INCLUDE_PATH=$TALIB_PREFIX/include 
ENV PYTHONPATH="$PYTHONPATH:$WORKDIR"
WORKDIR $WORKDIR

FROM base as poetry_installer
RUN apt-get install --no-install-recommends -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -

FROM base as dev
COPY --from=poetry_installer $POETRY_HOME $POETRY_HOME
