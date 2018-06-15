#Use an poldracklab/fitlins as a parent image
FROM poldracklab/fitlins

# Set the working directory to /work (should have been created by the fitlins paerent image)
WORKDIR /work

# Copy the current directory contents into the container at /app (using COPY instead of ADD to keep it lighter)
COPY [".", "/src/neuroscout"]

# Install additional neuroscout packages specified in requirements.txt
RUN /bin/bash -c "source activate neuro \
      && pip install -q --no-cache-dir -r /src/neuroscout/requirements.txt" \
    && sync

# Change entrypoint to neuroscout so it doesn't hangup on fitlins
ENTRYPOINT ["/neurodocker/startup.sh", "fitlins", "neuroscout"]
