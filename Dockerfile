#ENSURE CLEANED_FLIGHTS.DB EXISTS OR IS CREATED BEFORE RUNNING THIS FILE
FROM python:3.11

WORKDIR /app

# Copy only the requirements file first for caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the Python path to the 'main' directory
ENV PYTHONPATH="/app/main"

EXPOSE 5001

#Start FastAPI server
CMD ["uvicorn", "main.app:app", "--host", "0.0.0.0", "--port", "5001"]