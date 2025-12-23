# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn explicitly (if not in requirements.txt)
RUN pip install gunicorn

# Copy the entire project
COPY . .

# Make sure the STATIC_ROOT folder exists
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Set PYTHONPATH so Python can find punch_minichat module
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the app with Gunicorn
CMD ["gunicorn", "punch_minichat.wsgi:application", "--bind", "0.0.0.0:8000"]

