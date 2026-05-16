# Use the official lightweight Python 3.11 base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the project configuration and source code
COPY pyproject.toml .
COPY src/ src/
COPY config/ config/

# Install the project in editable mode so __file__ paths resolve correctly
RUN pip install --no-cache-dir -e .

# Create empty data and logs directories to mount local volumes later
RUN mkdir -p data logs

# Set the timezone to UTC for consistent system time inside the container
ENV TZ="UTC"

# Tell Python where the source directory is
ENV PYTHONPATH="/app/src"

# Run the daemon process using the correct module name
CMD ["python", "-m", "data_pipeline", "daemon"]