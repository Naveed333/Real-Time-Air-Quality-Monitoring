# Use a base Python image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install necessary dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code to the container
COPY . /app/

# Expose the port Streamlit runs on
EXPOSE 8501

# Set default command to run the Streamlit app
CMD ["streamlit", "run", "streamlit_app/app.py"]
