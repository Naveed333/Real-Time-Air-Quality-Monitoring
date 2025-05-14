# Real-Time Air Quality Monitoring

## Project Overview

This project monitors real-time air quality using various sensors, processes the data using **Apache Kafka** and **Apache Spark**, and visualizes the data in **Grafana**. It uses **InfluxDB** to store the data and provides a **Streamlit** application for real-time visualization. The system provides data such as **PM2.5**, **PM10**, **CO** levels, **temperature**, **humidity**, and **Air Quality Index (AQI)**.

---

## Architecture

1. **Air Quality Sensors**: Collect data about air quality parameters such as PM2.5, PM10, CO, temperature, and humidity.
2. **Kafka Producer**: Sends data from sensors to **Apache Kafka** in real time.
3. **Kafka**: Acts as a message queue to stream data.
4. **Apache Spark**: Processes incoming data in real-time.
5. **InfluxDB**: Stores the processed data for time-series analysis.
6. **Streamlit**: Provides a real-time user interface to visualize air quality data.
7. **Grafana**: Offers a more advanced and customizable dashboard for monitoring air quality trends.

---

## Features

- Real-time streaming of air quality data using **Apache Kafka**.
- Data processing and analytics using **Apache Spark**.
- **InfluxDB** for storing time-series data.
- **Streamlit** web interface for real-time visualization of air quality data.
- **Grafana** for detailed data exploration and visualization.

---

## Getting Started

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.7+
- Docker and Docker Compose (for running services like Kafka, InfluxDB, Grafana)
- Apache Kafka (for message streaming)
- Apache Spark (for data processing)
- InfluxDB (for time-series data storage)
- Grafana (for visualization)
- **pip** for installing Python dependencies

---

### Setting Up the Environment

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/Naveed333/Real-Time-Air-Quality-Monitoring
    cd real-time-air-quality-monitoring
    ```

2. **Create and Activate a Virtual Environment**:

    ```bash
    python3 -m venv venv  # Create virtual environment
    source venv/bin/activate  # Activate it (for macOS/Linux)
    # or venv\Scripts\activate for Windows
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Start Docker Containers**:

    Use Docker Compose to start all services (Kafka, InfluxDB, Grafana, etc.):

    ```bash
    docker-compose up -d
    ```

    This will start the necessary services in the background.

---

### Running the Application

1. **Start the Kafka Producer**:

    The producer simulates the sensor data and sends it to Kafka.

    ```bash
    python data_ingestion/producer.py
    ```

2. **Start the Spark Consumer**:

    The consumer reads the data from Kafka, processes it, and writes it to **InfluxDB**.

    ```bash
    python air_quality_streaming.py
    ```

3. **Run Streamlit for Real-Time Visualization**:

    Start the Streamlit app to visualize the data in real-time.

    ```bash
    streamlit run streamlit_app/app.py
    ```

    This will open a Streamlit web interface at `http://localhost:8501`.

4. **Run Grafana for Advanced Monitoring**:

    - Open **Grafana** at `http://localhost:3000`.
    - Log in with the default credentials:
      - Username: `admin`
      - Password: `admin`
    - Set up **InfluxDB** as the data source and visualize the metrics in real-time.
      - Open **Influxdb** at http://localhost:8086
---
