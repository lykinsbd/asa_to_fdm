# Start with a Alpine based Python image
FROM python:alpine3.9

# Set a more helpful shell prompt
ENV PS1='[\u@\h \W]\$ '

# The python sdist filename includes the version, so
# each new build means a new version and a new tarball.
ARG version
ARG tarball

# Set Docker image metadata
LABEL name="ASA to FDM API Image" \
      maintainer="Brett Lykins <lykinsbd@gmail.com>" \
      author="Brett Lykins <lykinsbd@gmail.com>" \
      license="GPLv3+" \
      version="${version}"

# Put our stuff in the temp dir
COPY ["${tarball}", "requirements.txt", "gunicorn.py", "/tmp/"]

# Install all the things, below is a full breakdown of this monster RUN command:

# Update and upgrade all installed packages
# Install packages that are needed by some python libraries to compile successfully
# Install curl, it's needed for self-healthchecks
# Install requirements for our code
# Install our code
# Remove build dependencies (since it's built now)
# Create our /app directory for things to live in
# Move gunicorn.py into there
# Remove our temp directory

RUN apk update && apk upgrade --no-cache && \
    apk add --no-cache --virtual .build-deps build-base python3-dev libffi-dev openssl-dev && \
    apk add --no-cache curl && \
    pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    pip install --no-cache-dir --no-deps /tmp/$(basename ${tarball}) && \
    apk del .build-deps && \
    mkdir /app && \
    mv /tmp/gunicorn.py /app/gunicorn.py && \
    rm -fr /tmp

# Make our working dir "/app"
WORKDIR "/app"

# Export the version as an environment variable for possible logging/debugging
ENV API_VER ${version}

# Our code serves HTTP on port 5000. The dockervisor will expose this port
# to the world as some other number, set at run time.
EXPOSE 5000

# This container performs its own healthchecks by attempting to connect to
# our HTTP server and GET the healthcheck endpoint.
# Example of a successful response:
# {"status":200,"content":null,"message":"asa_to_fdm is running.","request_id":"2bef8456-c25b-4884-9250-9a0eeb4b4654"}
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD [ $APP_ENVIRONMENT = "staging" ] && staging="-staging"; \
    curl -k -f -H "Host: asa_to_fdm${staging}.localhost" http://127.0.0.1:5000/healthcheck

# When this container is run, it executes our code.
CMD ["gunicorn", "-c", "gunicorn.py", "asa_to_fdm.app:app"]
