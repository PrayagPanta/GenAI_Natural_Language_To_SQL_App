# Project Setup and Overview

## 1.Download the dataset and Initialize database.
Download the `2015-flight-delays-and-cancellation-prediction` dataset from Kaggle, extract the 3 csv files in `data` folder, and create
the `cleaned_flights.db` database using the provided Jupyter notebook.
Then, install required dependencies via `requirements.txt` file.

### Notes on Database Structure:

The database used in this project is a cleaned version of the dataset. However, this structure may not be optimal. A
thorough analysis of the use case is required to determine the appropriate fields and structure for the database based
on the CSV data.

The chosen structure is primarily for convenience and due to the lack of specific context. depending on your
application, you may need to adjust the database schema and consider creating necessary indexes.

## 2. Running the Project

The project can be executed by running the `app.py` file.

```bash
python app.py
```

## 3. Possible Improvements

1. **Prompt Evaluation & User Ratings:**
    - User ratings stored in `user_sessions.db` can be analyzed to identify the lowest-rated queries. Based on this
      analysis, prompt modifications can be made to improve user experience.

2. **RAG (Retrieval-Augmented Generation):**
    - Implement RAG for scenarios where query generation fails after multiple retries. PostgreSQL offers better support
      for such implementations.

3. **Unit & Integration Tests:**
    - Complete sets of Unit and integration tests should be added to ensure robustness. This was skipped due to time constraints but is
      essential for long-term maintainability.

5. **Database Indexes:**
    - Consider adding indexes to the database for performance optimization based on query patterns and requirements.

6. **Docker Compose:**
    - Add Docker Compose files to manage multi-container setups (e.g., database, application server) for easier
      development and deployment.

## 4.For Production Deployment:
## Recommended Cloud Infrastructure

### 1. **Database**
For production deployments, it's recommended to use dedicated SQL databases such as:

- **Azure SQL Database** (Azure)  
  _Equivalent: **Amazon Aurora** (AWS)_
  
Avoid using local databases like **SQLite**, which are not suitable for production-level scalability and performance.

### 2. **LLM Integration**
For improved completions and performance, use the **Azure OpenAI Service** instead of relying on free-tier models such as the **Gemini Flash 2.0**.

- **Azure OpenAI Service** (Azure)  
  _Equivalent: **Amazon Bedrock** (AWS)_

### 3. **App Deployment**
The FastAPI app can be deployed using Docker containers. Depending on the scale and traffic requirements, you can use the following services:

- **Azure App Service** (Azure)  
  _Equivalent: **Amazon Elastic Beanstalk** (AWS)_

- **Amazon ECS with Fargate** (AWS)  
  _Equivalent: **Azure Kubernetes Service (AKS)** (Azure)_

For lighter workloads, consider using **Azure Functions**, a serverless option that offers advanced scalability, load balancing, and enhanced security features.

- **Azure Functions** (Azure)  
  _Equivalent: **AWS Lambda** (AWS)_

## Deployment Steps

1. **Database Setup**:
   - Set up **Azure SQL Database** or **Amazon Aurora** for your application.
   - Configure the necessary connections and credentials in your app.

2. **Integrate LLM**:
   - Use the **Azure OpenAI Service** or **Amazon Bedrock** to integrate Large Language Models (LLMs) for better performance.

3. **Docker Deployment**:
   - Build your Docker image for the FastAPI app.
   - Push the Docker image to your chosen container registry (Azure Container Registry or Amazon ECR).

4. **Choose Deployment Platform**:
   - For **high scalability** and automatic management, deploy on **Azure App Service** or **Amazon Elastic Beanstalk**.
   - For container orchestration and scaling, deploy using **Azure Kubernetes Service (AKS)** or **Amazon ECS with Fargate**.
   - For **light traffic** and serverless scaling, deploy using **Azure Functions** or **AWS Lambda**.

5. **Security**:
   - Ensure that your app is secured with **SSL/TLS** and **IAM/RBAC** for access control.
   - Use **WAF** (Web Application Firewall) for added protection against threats.
   - **AWS WAF** (AWS)  
     _Equivalent: **Azure WAF** (Azure)_


---