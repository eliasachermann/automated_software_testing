# Start from the base image you want
FROM theosotr/sqlite3-test

# Set root user to install stuff
USER root

# Install Python
RUN apt-get update && apt-get install -y python3

# Copy the correct file
COPY sqlite-autoconf-3490100.tar /tmp/

# Build and install SQLite 3.49.1
RUN cd /tmp && \
    tar xf sqlite-autoconf-3490100.tar && \
    cd sqlite-autoconf-3490100 && \
    ./configure && \
    make && \
    cp sqlite3 /usr/bin/sqlite3-3.49.1 && \
    chmod +x /usr/bin/sqlite3-3.49.1 && \
    rm -rf /tmp/sqlite-autoconf-3490100*

# Set working directory for your project (this is where your code will live)
WORKDIR /app

# Done! The rest is handled by mounting your local project when you run the container
