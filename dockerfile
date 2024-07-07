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

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]