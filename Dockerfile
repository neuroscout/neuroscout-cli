FROM poldracklab/fitlins

# Set user back to root
USER root
RUN mkdir /data
RUN chown -R neuro /work /data

# Install neurodebian/datalad
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install datalad -yq

USER neuro

RUN git config --global user.name "Neuroscout"
RUN git config --global  user.email "user@example.edu"

# Copy the current directory contents into the container
COPY [".", "/src/neuroscout"]

USER root
RUN chown -R neuro /src
USER neuro

RUN /bin/bash -c "source activate neuro \
      && pip install --no-cache-dir -e /src/neuroscout/" \
    && sync

RUN /bin/bash -c "source activate neuro \
      && pip install -q --no-cache-dir --upgrade -r /src/neuroscout/requirements.txt" \
    && sync

WORKDIR /data

# Change entrypoint to neuroscout
ENTRYPOINT ["/neurodocker/startup.sh", "neuroscout"]
