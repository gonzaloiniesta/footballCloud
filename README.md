# 🏟️ **Football Cloud**

**Football Cloud** is a personal project designed to apply and enhance my skills in microservices architecture design and backend application development. The primary goal is to create a platform that provides real football match data for free via an API, using modern technologies and integrations to ensure efficient and accessible data flow.

The system automates the process of extracting data, publishing the raw data to a **Kafka** topic. From there, three main microservices handle the processing and exposure of the data:

1. **Scraper Microservice (Scraper-Service)**:  
   - Collects football match data using web scraping techniques.  
   - Publishes the raw data to a Kafka topic.  
   - Optionally saves the data as a local CSV file (`stats.csv`).

2. **Data Transformation Microservices (ETL-Services)**:  
   - Multiple ETL services consume raw data from the Kafka topic.  
   - Each service transforms, cleans, and stores the data in a **PostgreSQL** and/or **MongoDB** database.  
   - The ETL services are scalable, allowing multiple instances to process data in parallel for improved performance.

3. **REST API Microservice (API-Service)**:  
   - Provides RESTful endpoints developed with **FastAPI**.  
   - Allows external applications to query the processed data for analysis and visualization.

This project facilitates free access to football data through a modular and maintainable platform, leveraging technologies like **Docker**, **Kafka**, **PostgreSQL**, **MongoDB**, and **FastAPI** to efficiently integrate different services.

---

## 🌐 **Project Description**

The project focuses on three key stages:

1. **Data Collection (Scraper-Service)**:  
   - A dedicated service performs web scraping to capture match statistics.  
   - The raw data is published to a Kafka topic and optionally saved locally as `stats.csv`.

2. **Data Transformation (ETL-Services)**:  
   - Multiple ETL microservices consume data from Kafka.  
   - The data is cleaned, transformed, and stored in PostgreSQL or MongoDB.  
   - The ETL architecture supports horizontal scaling, allowing you to run multiple ETL instances to handle large volumes of data efficiently.

3. **Data Delivery (API-Service)**:  
   - A RESTful API developed with FastAPI provides access to the stored data.  
   - External applications can query and use the data for analysis and visualization.

---

## 🏗️ **System Architecture**

![Football Cloud Architecture](arquitectura_fclouf.png)

### **Workflow Explanation**

1. **`Scraper-Service`**  
   - **Function**: Collects football match data using web scraping techniques with Selenium.  
   - **Output**: Publishes the raw data (in bytes) to a Kafka topic and optionally saves it as a local CSV file (`stats.csv`).  
   - **Execution**: Runs locally due to the requirement of having Google Chrome installed.

2. **Kafka**  
   - **Function**: Acts as a message broker to handle asynchronous communication between the `Scraper-Service` and the `ETL-Services`.  
   - **Topic**: Temporarily stores the raw data, allowing the scraping process to be decoupled from data transformation.

3. **`ETL-Services`**  
   - **Function**:  
     - Consume data from the Kafka topic.  
     - Clean, transform, and format the data.  
     - Store the processed data in PostgreSQL and/or MongoDB.  
     - **Scalability**: Multiple ETL instances can run in parallel to handle large datasets.

4. **`API-Service`**  
   - **Function**: Provides HTTP endpoints to query and retrieve the stored data from PostgreSQL or MongoDB.  
   - **Technology**: Developed with FastAPI for efficient and scalable access to the data.

---

## 🚀 **Features**

- **Manual Web Scraping**: Collect football data using Selenium and Chrome Headless.
- **Asynchronous Communication**: Kafka enables scalable and decoupled data processing.
- **Scalable ETL Pipeline**: Run multiple ETL instances to process large volumes of data.
- **RESTful API**: FastAPI provides easy access to the processed data.
- **Flexible Data Storage**: PostgreSQL for structured data and MongoDB for JSON-based storage.

---

## 🛠️ **Technologies Used**

- **Web Scraping**: `Selenium` with `Chrome Headless`
- **Message Broker**: `Apache Kafka`
- **API Framework**: `FastAPI`
- **Databases**: `PostgreSQL` and `MongoDB`
- **Containerization**: `Docker` and `Docker Compose`
- **Programming Language**: `Python`

---

## 🚀 **How to Run the Project**

### 1. Clone the Repository

```bash
git clone https://github.com/gonzaloiniesta/footballCloud.git
cd footballCloud
