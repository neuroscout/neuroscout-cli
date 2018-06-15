# Use an poldracklab/fitlins as a parent image
FROM poldracklab/fitlins

# Copy the current directory contents into the container at /app (using COPY instead of ADD to keep it lighter)
COPY [".", "/src/neuroscout"]

USER root

# User-defined instruction
RUN chown -R neuro /src /work

USER neuro

# Install additional neuroscout packages specified in requirements.txt
RUN /bin/bash -c "source activate neuro \
      && pip install -q --no-cache-dir -r /src/neuroscout/requirements.txt" \
    && sync

RUN /bin/bash -c "source activate neuro \
      && pip install -q --no-cache-dir -e /src/neuroscout/" \
    && sync

WORKDIR /work

RUN /bin/bash -c "source activate neuro"

# Change entrypoint to neuroscout so it doesn't hangup on fitlins
ENTRYPOINT ["neuroscout"]
