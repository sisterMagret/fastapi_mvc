# Use the official Python image from Docker Hub
FROM python:3.13-slim

# Set the working directory
WORKDIR /src

# Install pipenv
RUN pip install --upgrade pip && \
    pip install pipenv

# Copy Pipfile and Pipfile.lock (if available)
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv
RUN pipenv install --system --deploy

# Copy the FastAPI code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
