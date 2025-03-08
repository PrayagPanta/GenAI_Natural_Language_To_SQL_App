FROM python:3.11

WORKDIR /app

# Copy only the requirements file first for caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install Kaggle, download and extract the dataset into the data folder.
# Note: Ensure you have configured Kaggle API credentials if required.
RUN pip install --no-cache-dir kaggle && \
    mkdir -p data && \
    kaggle competitions download -c 2015-flight-delays-and-cancellation-prediction -p data --unzip

# Install Jupyter and nbconvert so we can execute the notebook
RUN pip install --no-cache-dir jupyter nbconvert

COPY . .

EXPOSE 5001

# Use exec form to execute notebook first, then start FastAPI server
CMD ["sh", "-c", "jupyter nbconvert --to notebook --execute 2015-flight-delays-and-cancellation-prediction.ipynb && python main/app.py"]
