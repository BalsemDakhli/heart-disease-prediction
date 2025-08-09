# Step 1: Use an official Python runtime as base image
FROM python:3.10-slim

# Step 2: Set working directory inside the container
WORKDIR /app

# Step 3: Copy all files from your local 'flask/' to '/app' in the container
COPY . .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose port (Flask default)
EXPOSE 5000

# Step 6: Command to run the Flask app
CMD ["python", "app.py"]
