FROM poldracklab/fitlins:master

# Set user back to root
USER root
RUN mkdir /data

# Install neurodebian/datalad
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install datalad -yq

RUN git config --global user.name "Neuroscout"
RUN git config --global  user.email "user@example.edu"

# Copy the current directory contents into the container
COPY [".", "/src/neuroscout"]

RUN /bin/bash -c "source activate neuro \
      && pip install -q --no-cache-dir -e /src/neuroscout/" \
    && sync

RUN /bin/bash -c "source activate neuro \
      && pip install -q --no-cache-dir --upgrade -r /src/neuroscout/requirements.txt" \
    && sync

WORKDIR /data

# Change entrypoint to neuroscout
ENTRYPOINT ["/neurodocker/startup.sh", "neuroscout"]
