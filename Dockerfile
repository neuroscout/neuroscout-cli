# Use an poldracklab/fitlins as a parent image
FROM poldracklab/fitlins

# Set user back to root
USER root
RUN chown -R root /src /work
RUN mkdir /data

# Install neurodebian/datalad
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install datalad -yq

RUN git config --global user.name "Neuroscout"
RUN git config --global  user.email "user@example.edu"


# Install additional neuroscout + dependencies
RUN /bin/bash -c "source activate neuro \
      && pip install -q --no-cache-dir -e git+https://github.com/poldracklab/fitlins.git@cceba1a46#egg=fitlins" \
    && sync

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
