FROM theosotr/sqlite3-test

USER root

RUN apt-get update && apt-get install -y \
    python3 \
    gcc \
    g++ \
    make \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://www.sqlite.org/2018/sqlite-autoconf-3260000.tar.gz -O /tmp/sqlite-autoconf-3260000.tar.gz

RUN cd /tmp && \
    tar xzf sqlite-autoconf-3260000.tar.gz && \
    cd sqlite-autoconf-3260000 && \
    ./configure CFLAGS="-fprofile-arcs -ftest-coverage -O0" CXXFLAGS="-fprofile-arcs -ftest-coverage -O0" LDFLAGS="--coverage" && \
    make

RUN cp /tmp/sqlite-autoconf-3260000/sqlite3 /usr/bin/sqlite3-3.26.0

COPY sqlite-autoconf-3490100.tar /tmp/

RUN cd /tmp && \
    tar xf sqlite-autoconf-3490100.tar && \
    cd sqlite-autoconf-3490100 && \
    ./configure CFLAGS="-O0" CXXFLAGS="-O0" && \
    make

RUN cp /tmp/sqlite-autoconf-3490100/sqlite3 /usr/bin/sqlite3-3.49.1

WORKDIR /app

COPY fuzzer.py /app/

RUN echo '#!/bin/sh\ncd /app\nexec python3 /app/fuzzer.py "$@"' > /bin/test-db && \
    chmod +x /bin/test-db


WORKDIR /app
