FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code from the host folder "app" into /app in the container
COPY app/ .    

# <-- THIS is crucial

EXPOSE 5000

CMD ["python", "app.py"]
