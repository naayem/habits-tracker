# Habit Tracker App

**Personal Project based on the Science of Habits**

An application designed to help reinforce good habits, based on the principles of habit science.

## Features

- **Daily Habit Tracking**: Log daily activities to monitor progress and build consistent habits.
- **Streak Visualization**: Track habit streaks to stay motivated.
- **Analytics**: Utilize pandas and numpy to provide insights into habit patterns over time.
- **Cloud Storage**: Stores data securely using Supabase for easy access and retrieval.

## Technologies Used

- **Python 3.10**: Core programming language for the app.
- **Streamlit**: Provides an easy-to-use interface for tracking and visualizing habits.
- **Supabase**: A backend-as-a-service to store and manage user data.
- **pandas**: Data manipulation and analysis to generate habit tracking statistics.
- **numpy**: Supports numerical computations for detailed habit analysis.
- **pyyaml**: Handles configuration settings efficiently.
- **logger**: Manages logging to track app activities and debugging.
- **pytest**: Used for testing to ensure code reliability and correctness.
- **Docker**: Containerizes the application for easy deployment.

## Getting Started

### Clone the repository

```bash
git clone https://github.com/naayem/habits-tracker.git
cd habits-tracker
```

### Using Poetry

1. **Install dependencies**:
   ```bash
   poetry install
   ```
2. **Run the application**:
   ```bash
   poetry run streamlit run app.py
   ```

### Using Docker

1. **Build the Docker image**:
   ```bash
   docker build -t habits-tracker .
   ```

2. **Run the Docker container**:
   ```bash
   docker run -p 8501:8501 habits-tracker
   ```

3. **Access the app**: Open your browser and navigate to `http://localhost:8501`.

### Dockerfile Example

Here's an example Dockerfile that you can include in the project for reference:

```Dockerfile
# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy pyproject.toml and poetry.lock to the working directory
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Install the dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the rest of the application code to the container
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py"]
```

## Why This App?

Building and maintaining habits is crucial for self-improvement. This app, inspired by habit science, provides tools to track and analyze your habits, encouraging consistency and positive change.

## License

This project is open-source and available under the [MIT License](./LICENSE).
