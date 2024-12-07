# 🏟️ **Football Cloud**

Football Cloud is a personal project aimed at applying my skills in programming, data analysis, and system development. This project focuses on the statistical analysis of football matches using modern microservices architecture, Kafka, and MongoDB.

---

## 📊 **System Architecture**

![Football Cloud Architecture](attachment:images/architecture-footballCloud.png)

### **Workflow Explanation**

1. **`Scraper-Service`**:
   - **Function**: Collects football match data from sources like LaLiga's website using web scraping techniques.
   - **Output**: Publishes the scraped data to a Kafka topic and optionally saves it as a local CSV file (`stats.csv`).

2. **Kafka**:
   - **Function**: Acts as a message broker to handle the communication between the `Scraper-Service` and the `ETL-Service`.
   - **Topic**: Stores the scraped data temporarily, allowing the system to decouple the scraping process from data transformation.

3. **`ETL-Service`**:
   - **Function**: Consumes data from the Kafka topic, transforms it (cleaning, formatting), and loads the processed data into MongoDB.
   - **Data Storage**: Saves the cleaned and transformed data into a MongoDB database.

4. **`API-Service`**:
   - **Function**: Provides HTTP endpoints to query and retrieve the stored data from MongoDB.
   - **Usage**: These endpoints can be used by frontend applications or external tools to display football statistics and insights.

---

## 🚀 **Features**

- **Web Scraping**: Automated collection of football data using Selenium and Chrome Headless.
- **Asynchronous Communication**: Kafka enables scalable and decoupled data processing.
- **Data Transformation**: ETL pipeline ensures data is cleaned and ready for analysis.
- **RESTful API**: FastAPI-powered service to access the data easily.
- **Data Storage**: MongoDB stores data in flexible JSON format for efficient querying.

---

## 🛠️ **Technologies Used**

- **Web Scraping**: `Selenium` with `Chrome Headless`
- **Message Broker**: `Apache Kafka`
- **API Framework**: `FastAPI`
- **Database**: `MongoDB`
- **Containerization**: `Docker` and `Docker Compose`
- **Data Analysis**: `Pandas`
- **Visualization**: (Future) `React` or `Vue.js`

---

## 🚀 **How to Run the Project**

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/football-cloud.git
cd football-cloud
