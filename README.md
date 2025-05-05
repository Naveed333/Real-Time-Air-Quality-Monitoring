# Real-Time Air Quality Monitoring and Alert System

An end-to-end data engineering pipeline to monitor air quality in real-time using public APIs, Kafka, Spark, Airflow, ML, and Streamlit.

## ✅ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-repo/air-quality-monitoring.git
cd air-quality-monitoring
```

### 2. Set up environment variables
```bash
cp config/secrets.env.example config/secrets.env
```
Edit with your actual OpenAQ API key.

### 3. Install dependencies (for local testing)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run Docker containers
```bash
cd docker
docker-compose up --build
```

### 5. Start the Producer (optional in separate terminal)
```bash
cd api_ingestion
python producer.py
```

### 6. Access services
- **Streamlit Dashboard:** http://localhost:8501
- **Airflow UI:** http://localhost:8080 (default user: airflow / airflow)
- **Kafka Broker:** localhost:9092

### 7. Run Spark job manually
```bash
cd data_processing
spark-submit spark_job.py
```

### 8. Trigger ML pipeline manually
```bash
cd ml_model
python train_model.py
python predict.py
```

## 🧪 Testing
You can write test cases using `pytest` under a `/tests` directory.

## 🔒 Security
Store secrets (API keys, credentials) in `config/secrets.env` and load them safely using environment variables.