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
RUN poetry lock [--no-update]
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Install necessary software
RUN apt-get update && \
    apt-get -y install cron

# Add crontab file
COPY crontab /etc/cron.d/crontab

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8501

# Run cron and Streamlit together
CMD service cron start && streamlit run app.py
