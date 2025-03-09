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
    - Implement RAG for scenarios where query generation fails after multiple retries. PostgreSQL with PgVector offers better support
      for such implementations.

3. **Unit & Integration Tests:**
    - Only a sample of unit tests has been added. However, Complete sets of Unit and integration tests should be added to ensure robustness.

5. **Database Indexes:**
    - Consider adding indexes to the database for performance optimization based on query patterns and requirements.


## Deployment Steps and Recommended Cloud Infrastructure

1. **Database Setup**:
   - Avoid using local databases like SQLite, which are not suitable for production-level scalability and performance.
   - Set up **Azure SQL Database** or **Amazon Aurora** for your application.
   - Configure the necessary connections and credentials in your app.

2. **Integrate LLM**:
   - Use the **Azure OpenAI Service** or **Amazon Bedrock** to integrate Large Language Models (LLMs) for better performance.
   - Free-tier models such as the **Gemini Flash 2.0** are only good enough for demo purposes. Alternatively, you can even fine-tune your own open-source models.

3. **Docker Deployment**:
   - Build your Docker image for the FastAPI app.
   - Push the Docker image to your chosen container registry (Azure Container Registry or Amazon ECR).

4. **Choose Deployment Platform**:
   - For **high scalability** and automatic management, deploy on **Azure App Service** or **Amazon Elastic Beanstalk**.
   - For container orchestration and scaling, deploy using **Azure Container Instance** or **Azure Kubernetes Service (AKS)** or **Amazon ECS with Fargate**.
   - For **light traffic** and serverless scaling, deploy using **Azure Functions** or **AWS Lambda**.

5. **Security**:
   - Ensure that your app is secured with **SSL/TLS** and **IAM/RBAC** for access control.
   - Use **WAF** (AWS Web Application Firewall) or **Azure WAF** for added protection against threats.

---