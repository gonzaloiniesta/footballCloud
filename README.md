# 🏟️ **Football Cloud**

**Football Cloud** is a professional project focused on developing a microservices architecture for the collection, transformation, and delivery of football match data. The system automates the process of extracting information manually from LaLiga's official website, transforming it, and exposing it via an API for use in external applications and advanced analysis.

The primary goal is to build a robust infrastructure that facilitates efficient data processing while ensuring modularity, scalability, and maintainability.

---

## 🌐 **Project Description**

The project focuses on three key stages:

1. **Data Collection**:  
   A dedicated service performs web scraping on LaLiga's official website, capturing match statistics manually.

2. **Data Transformation**:  
   The collected data is sent through Kafka, where an ETL microservice consumes, cleans, transforms, and stores it in a NoSQL database (MongoDB).

3. **Data Delivery**:  
   A RESTful API provides access to the stored data, allowing other applications or systems to efficiently query and use the information.

---

## 🏗️ **System Architecture**

![Football Cloud Architecture](images/architecture-footballCloud.png)

### **Workflow Explanation**

1. **`Scraper-Service`**  
   - **Function**: Collects football match data manually from LaLiga's official website using web scraping techniques with Selenium.  
   - **Output**: Publishes the raw data (in bytes) to a Kafka topic and optionally saves it as a local CSV file (`stats.csv`).  
   - **Execution**: Runs locally due to the requirement of having Google Chrome installed.

2. **Kafka**  
   - **Function**: Acts as a message broker to handle asynchronous communication between the `Scraper-Service` and the `ETL-Service`.  
   - **Topic**: Temporarily stores the raw data, allowing the scraping process to be decoupled from data transformation.

3. **`ETL-Service`**  
   - **Function**:  
     - Consumes data from the Kafka topic.  
     - Cleans, transforms, and formats the data.  
     - Stores the processed data in MongoDB.

4. **`API-Service`**  
   - **Function**: Provides HTTP endpoints to query and retrieve the stored data from MongoDB.  
   - **Technology**: Developed with FastAPI for efficient and scalable access to the data.

---

## 🚀 **Features**

- **Manual Web Scraping**: Collect football data using Selenium and Chrome Headless.
- **Asynchronous Communication**: Kafka enables scalable and decoupled data processing.
- **Data Transformation**: ETL pipeline ensures data is cleaned and structured for analysis.
- **RESTful API**: FastAPI provides easy access to the processed data.
- **Flexible Data Storage**: MongoDB stores data in JSON format for efficient querying.

---

## 🛠️ **Technologies Used**

- **Web Scraping**: `Selenium` with `Chrome Headless`
- **Message Broker**: `Apache Kafka`
- **API Framework**: `FastAPI`
- **Database**: `MongoDB`
- **Containerization**: `Docker` and `Docker Compose`
- **Programming Language**: `Python`
- **Data Analysis**: `Pandas`
- **Visualization**: (Future) `React` or `Vue.js`

---

## 🚀 **How to Run the Project**

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/football-cloud.git
cd football-cloud
