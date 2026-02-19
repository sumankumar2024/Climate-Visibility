FROM python:3.10-slim

# Install AWS CLI AND git
RUN apt-get update && apt-get install -y \
    awscli \
    git \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

# 1. Copy ONLY requirements first
COPY requirements.txt .

# 2. Install dependencies 
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 3. Copy the rest of the application code
COPY . .

# 4. Expose the port your Flask app runs on
EXPOSE 8062

# 5. Run the app using a production server (Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8062", "app:app"]