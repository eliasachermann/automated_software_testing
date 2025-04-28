FROM theosotr/sqlite3-test

USER root

# Install build tools
RUN apt-get update && apt-get install -y \
    python3 \
    gcc \
    g++ \
    make \
    wget \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------
# Build and install SQLite 3.26.0 with coverage flags
# -------------------------------------------------

# Download the 3.26.0 source tarball
RUN wget https://www.sqlite.org/2018/sqlite-autoconf-3260000.tar.gz -O /tmp/sqlite-autoconf-3260000.tar.gz


# Extract, configure with coverage, and build
RUN cd /tmp && \
    tar xzf sqlite-autoconf-3260000.tar.gz && \
    cd sqlite-autoconf-3260000 && \
    ./configure CFLAGS="-fprofile-arcs -ftest-coverage" CXXFLAGS="-fprofile-arcs -ftest-coverage" LDFLAGS="--coverage" && \
    make

# Save the compiled binary as sqlite3-3.26.0
RUN cp /tmp/sqlite-autoconf-3260000/sqlite3 /usr/bin/sqlite3-3.26.0

# -------------------------------------------------
# Build and install SQLite 3.49.1 (normal build)
# -------------------------------------------------

# Copy your 3.49.1 tarball into the image
COPY sqlite-autoconf-3490100.tar /tmp/

# Extract, configure normally, and build
RUN cd /tmp && \
    tar xf sqlite-autoconf-3490100.tar && \
    cd sqlite-autoconf-3490100 && \
    ./configure && \
    make

# Save the compiled binary as sqlite3-3.49.1
RUN cp /tmp/sqlite-autoconf-3490100/sqlite3 /usr/bin/sqlite3-3.49.1

# -------------------------------------------------
# Set the working directory for your project
# -------------------------------------------------
WORKDIR /app
