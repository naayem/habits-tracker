# Use the official Python image from the Docker Hub
FROM python:3.12

# Set PIP_DEFAULT_TIMEOUT environment variable
ENV PIP_DEFAULT_TIMEOUT=100

# Set the working directory
WORKDIR /habits_tracker

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

# Copy poetry files and install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy the rest of the application
COPY . .

# Create cron log file
RUN touch /var/log/cron.log \
    && chmod 0644 /var/log/cron.log

# Create a directory for custom cron jobs
RUN mkdir -p /etc/cron.d

# Add the cron job

# Add the cron jobs
RUN echo "30 9 * * * /usr/local/bin/python /habits_tracker/morning_routine.py >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron-job \
    && echo "0 9 * * * /usr/local/bin/python /habits_tracker/morning_warning.py >> /var/log/cron.log 2>&1" >> /etc/cron.d/my-cron-job \
    && echo "30 13 * * * /usr/local/bin/python /habits_tracker/morning_warning.py >> /var/log/cron.log 2>&1" >> /etc/cron.d/my-cron-job \
    && chmod 0644 /etc/cron.d/my-cron-job

# Apply cron job
RUN crontab /etc/cron.d/my-cron-job

# Expose port
EXPOSE 8501

# Copy the startup script
COPY start.sh .

# Ensure the startup script has execute permissions
RUN chmod +x start.sh

# Run the startup script
CMD ["./start.sh"]
