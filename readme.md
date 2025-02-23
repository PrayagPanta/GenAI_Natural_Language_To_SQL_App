
# Project Setup and Overview

## 1. Install Kaggle API
First, install the Kaggle API using pip:

```bash
pip install kaggle
```

Then, download the "2015-flight-delays-and-cancellation-prediction" dataset from Kaggle, extract the files, and create the `cleaned_flights.db` database using the provided Jupyter notebook.
Then, install required dependencies via requirements.txt file.

### Notes on Database Structure:
The database used in this project is a cleaned version of the dataset. However, this structure may not be optimal. A thorough analysis of the use case is required to determine the appropriate fields and structure for the database based on the CSV data.

The chosen structure is primarily for convenience and due to the lack of specific context. Depending on your application, you may need to adjust the database schema and consider creating necessary indexes.

## 2. Running the Project
The project can be executed by running the `app.py` file.

```bash
python app.py
```

## 3. Possible Improvements

1. **Prompt Evaluation & User Ratings:**
   - User ratings stored in `user_sessions.db` can be analyzed to identify the lowest-rated queries. Based on this analysis, prompt modifications can be made to improve user experience.
   
2. **RAG (Retrieval-Augmented Generation):**
   - Implement RAG for scenarios where query generation fails after multiple retries. PostgreSQL offers better support for such implementations.

3. **Unit & Integration Tests:**
   - Unit and integration tests should be added to ensure robustness. This was skipped due to time constraints but is essential for long-term maintainability.

4. **Database Indexes:**
   - Consider adding indexes to the database for performance optimization based on query patterns and requirements.

5. **Dockerization:**
   - Dockerize the implementation to simplify deployment and ensure consistency across environments.

6. **Docker Compose:**
   - Add Docker Compose files to manage multi-container setups (e.g., database, application server) for easier development and deployment.

---