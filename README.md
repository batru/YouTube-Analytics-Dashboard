## **YouTube Analytics Pipeline**

### **Project Overview: YouTube Channel Analytics Dashboard**

In the creator economy, YouTube content creators need robust insights to optimize their content strategies. YouTube's native dashboard provides basic metrics but lacks the flexibility and depth required for advanced analysis. This project implements a custom analytics pipeline that automates data collection, transformation, storage, and visualization—providing a centralized and actionable analytics platform.

---

### **Problem Addressed**

Creators often face challenges such as:
- Limited visibility into long-term trends
- Manual, error-prone data handling
- Lack of tailored, in-depth insights for decision-making

This pipeline addresses those issues by automating the entire process of data extraction, transformation, and visualization, enabling consistent and scalable analytics.

---

### **Implemented Features**

- ✅ **Data Extraction**: Used the YouTube API to pull video metadata, views, likes, comments, and publish timestamps.  
- ✅ **Data Transformation**: Processed raw data with Apache Spark to clean, normalize, and calculate key engagement metrics.  
- ✅ **Data Storage**: Loaded the transformed data into a PostgreSQL database hosted on Aiven.  
- ✅ **Workflow Scheduling**: Automated daily and weekly data syncs using Apache Airflow.  
- ✅ **Data Visualization**: Created a Grafana dashboard to visualize channel performance metrics.

---

### **Key Questions Answered by the Dashboard**

- 📈 How has the channel grown over time?  
- 🎥 Which videos perform best by engagement (likes/comments/views)?  
- ⏱️ What days and times work best for publishing content?  
- 🧑‍🤝‍🧑 What audience patterns or behaviors are visible?  
- 📅 Can weekly summaries of channel activity be generated automatically?  

Example channels used for testing: [`@cristiano`](https://youtube.com/@cristiano) and [`@luxtechacademy`](https://youtube.com/@luxtechacademy).

---

### **Outcomes**

- A self-updating PostgreSQL table containing structured performance data  
- Scheduled Airflow DAGs that run daily and weekly  
- An interactive Grafana dashboard featuring:
  - Time-series analytics  
  - Engagement heatmaps  
  - Top content breakdowns  
  - Summary statistics and KPIs

---


### **Dashboard Preview**

The Grafana dashboard visualizes channel performance metrics in real time:

![Dashboard Screenshot](https://github.com/batru/YouTube-Analytics-Dashboard/blob/main/dashboard.PNG?raw=true)

---

### **Technologies Used**

- Python  
- PostgreSQL (hosted on Aiven)  
- Apache Spark  
- Apache Airflow  
- Grafana  
- Git & GitHub
