# Use an poldracklab/fitlins as a parent image
FROM markiewicz/fitlins

# Copy the current directory contents into the container at /app (using COPY instead of ADD to keep it lighter)
COPY [".", "/src/neuroscout"]

# Set user back to root
USER root
RUN chown -R root /src /work

# USER neuro

# Install additional neuroscout + dependencies
RUN /bin/bash -c "source activate neuro \
      && pip install -q --no-cache-dir -r /src/neuroscout/requirements.txt" \
    && sync

RUN /bin/bash -c "source activate neuro \
      && pip install -q --no-cache-dir -e /src/fitlins[all]" \
    && sync

RUN /bin/bash -c "source activate neuro \
      && pip install -q --no-cache-dir -e /src/neuroscout/" \
    && sync

WORKDIR /work

# Change entrypoint to neuroscout
ENTRYPOINT ["/neurodocker/startup.sh", "neuroscout"]
