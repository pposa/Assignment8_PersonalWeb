FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install runtime dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
