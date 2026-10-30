
# 1. Use Python 3.11 as the base image
FROM python:3.11-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy dependency file
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy project files
COPY app.py .
COPY workflow.py .
COPY test_workflow.py .

# 6. Expose Streamlit port
EXPOSE 8501

# 7. Run Streamlit application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
