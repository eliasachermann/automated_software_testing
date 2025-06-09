FROM theosotr/sqlite3-test

USER root

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install sqlglot

RUN pip3 install --upgrade sqlglot

WORKDIR /app

COPY reducer.py /app/

RUN echo '#!/bin/sh\ncd /app\nexec python3 /app/reducer.py "$@"' > /bin/reducer && \
    chmod +x /bin/reducer


WORKDIR /app