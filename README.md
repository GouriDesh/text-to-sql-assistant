# Text-to-SQL Assistant

A natural language to SQL query assistant powered by **OpenAI GPT-4o-mini**. This application translates plain English questions into optimized executable SQL queries, executes them against a SQLite database, and returns clear conversational answers.

Built as a group project (**Group 02**) to explore practical, lightweight Generative AI application development through prompt engineering, LLM API integration, schema-aware in-context learning, and agentic self-correction.

**Team**

- Raquel Amarins
- Patricia Atkinson
- Gouri Deshpande
- Tiffany Huynh

---

## 1. Project Overview

This project bridges the gap between complex relational databases and non-technical users. Instead of manually writing SQL queries, users can ask questions in plain English and receive accurate answers generated directly from a relational database.

## Core Features

- **Schema Extraction** – Reads the Chinook database structure (tables, columns, and data types) and formats it into a schema-aware prompt for the language model.

- **Natural Language Parsing** – Leverages GPT-4o-mini to interpret user questions and map requests to the underlying database schema.

- **Automated SQL Generation with Self-Correction** – Generates SQL queries and automatically retries failed queries by sending the SQL error back to the language model for correction (up to three attempts).

- **Synthesis & Output** – Executes validated SQL queries against a read-only SQLite database and returns conversational responses.

### Example Questions

- *Which artist has the most albums?*
- *What are the top 5 genres by number of tracks?*
- *How many customers are from the USA?*

---

## Technical Stack

| Component | Technology |
|-----------|------------|
| LLM | OpenAI GPT-4o-mini |
| Database | SQLite |
| Dataset | Chinook Database |
| Prompting | Schema-aware Prompt Engineering |
| Safety | SQL Validation Module |
| Environment | python-dotenv |
| Language | Python |

The project uses the **Chinook** sample database, a well-known SQLite database representing a digital music store containing artists, albums, tracks, playlists, invoices, employees, and customers.

---

## 2. Repository Structure

```text
text-to-sql-assistant/
│
├── configs/
│   └── model_config.yaml              # Model configuration and parameters
│
├── data/
│   ├── .gitkeep
│   └── Chinook_Sqlite.sqlite          # Chinook sample SQLite database
│
├── docs/
│   ├── evaluation_framework.md        # Evaluation methodology
│   └── model_selection.md             # Model comparison and selection
│
├── experiments/
│   ├── core_pipeline.ipynb
│   ├── evaluation.ipynb
│   ├── model_test_qwen.ipynb
│   ├── model_test_sqlcoder.ipynb
│   ├── model_test_sqlcoder_gpu.ipynb
│   ├── phase1_setup.ipynb
│   └── schema_extraction.ipynb
│
├── models/
│
├── outputs/
│   ├── samples_20260724_014747.json
│   └── README.md
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── model_runner.py
│   └── sql_safety.py
│
├── utils/
│   ├── __init__.py
│   └── helpers.py
│
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
```

## Directory Overview

| Directory | Purpose |
|-----------|---------|
| **configs/** | Stores model configuration files and parameters. |
| **data/** | Contains the Chinook SQLite database used for query execution. |
| **docs/** | Documentation describing the evaluation framework and model selection process. |
| **experiments/** | Development notebooks used throughout the project lifecycle for experimentation and evaluation. |
| **models/** | Stores model-related resources and experiments. |
| **outputs/** | Contains representative generated outputs from the application. |
| **src/** | Core application code, including data loading, SQL generation, validation, and pipeline execution. |
| **utils/** | Shared helper functions used across the project. |

## 3. Environment Setup Guide

These instructions will help you set up and run the Text-to-SQL Assistant on your local machine. Before starting, ensure you have Python installed and an active OpenAI API key.

## Prerequisites

Before cloning the repository, make sure you have:

- Python 3.12 or newer
- Git
- An OpenAI API key with available credits
- Internet access for installing Python packages

---

## Windows (Git Bash)

Git Bash is recommended because it provides commands similar to macOS and Linux.

```bash
# Navigate to your preferred workspace
cd /c/Users/<your-username>/Documents

# Clone the repository
git clone https://github.com/GouriDesh/text-to-sql-assistant.git

# Enter the project directory
cd text-to-sql-assistant

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/Scripts/activate

# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Create a local environment file
touch .env
```

---

## macOS

```bash
# Navigate to your preferred workspace
cd ~/Documents

# Clone the repository
git clone https://github.com/GouriDesh/text-to-sql-assistant.git

# Enter the project directory
cd text-to-sql-assistant

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create a local environment file
touch .env
```

---

## Linux

The installation process is the same as macOS.

```bash
cd ~/Documents

git clone https://github.com/GouriDesh/text-to-sql-assistant.git

cd text-to-sql-assistant

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

touch .env
```

---

## Configure Your OpenAI API Key

Create a file named `.env` in the project's root directory and add your personal OpenAI API key.

```text
OPENAI_API_KEY=your-api-key-here
```

The application automatically loads this key using **python-dotenv**, so no additional configuration is required.

---

## Running the Application

After completing the setup, execute the application with:

```bash
python -m src.model_runner
```

Running this command performs the complete Text-to-SQL workflow:

1. Loads the Chinook SQLite database.
2. Extracts the database schema.
3. Builds a schema-aware prompt.
4. Sends the prompt to GPT-4o-mini.
5. Generates an SQL query.
6. Validates the SQL using the safety module.
7. Executes the query against the database.
8. If necessary, retries failed SQL generation using the self-correction loop.
9. Displays the results and saves representative outputs in the `outputs/` directory.

---

## Returning to the Project

Whenever you return to work on the project:

```bash
cd text-to-sql-assistant

git pull
```

Activate the virtual environment:

**Windows**

```bash
source venv/Scripts/activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

When you are finished working:

```bash
deactivate
```

---

## Database

This project uses the **Chinook SQLite** sample database.

If the database file is not included in your cloned repository, download it from the official Chinook repository:

https://github.com/lerocha/chinook-database

Place the database file in the following directory:

```text
data/
└── Chinook_Sqlite.sqlite
```

---

## Updating Dependencies

If new Python packages are installed during development, update the dependency list with:

```bash
pip freeze > requirements.txt
```

Commit the updated dependency file:

```bash
git add requirements.txt

git commit -m "Update requirements"

git push
```

---

## 4. API Key Safety Practices

Your OpenAI API key is tied to your account and billing information. Treat it like a password and never expose it publicly.

## Team Guidelines

### 1. Never commit your `.env` file.

The repository's `.gitignore` excludes `.env` by default. Keep your API key only on your local machine.

---

### 2. Each contributor should use their own API key.

Create a local `.env` file containing:

```text
OPENAI_API_KEY=your-personal-api-key
```

---

### 3. Never hardcode API keys.

Do not place API keys inside:

- Python source files
- Jupyter notebooks
- Documentation
- Git commits
- Public repositories

---

### 4. Set usage limits.

Configure spending limits through your OpenAI account to prevent unexpected charges caused by accidental or excessive API usage.

---

### 5. Replace compromised keys immediately.

If an API key is accidentally exposed:

1. Revoke the compromised key.
2. Generate a new API key.
3. Update your local `.env` file.

---

### 6. Verify before pushing code.

Before every commit, verify that `.env` is not being tracked.

```bash
git status
```

Only commit project files—never your API credentials.

---

## Environment Variables

The application automatically loads environment variables using **python-dotenv**.

Example:

```text
OPENAI_API_KEY=your-api-key-here
```

Once your `.env` file has been created, no further configuration is required.
## 5. System Architecture

The Text-to-SQL Assistant follows a modular pipeline that converts a user's natural language question into an executable SQL query, validates the generated SQL, executes it against the Chinook SQLite database, and returns a conversational response.

The workflow is illustrated below.

```text
User Question (Plain English)
        │
        ▼
Database & Schema Loader
        │
        ▼
Schema-Aware Prompt Builder
        │
        ▼
OpenAI GPT-4o-mini
        │
        ▼
Generated SQL Query
        │
        ▼
SQL Safety Validation
        │
        ▼
SQLite Query Execution
        │
   ┌────┴────┐
   │         │
Success   Failure
   │         │
   │         ▼
   │   Self-Correction Loop
   │   ├── Returns SQL error message
   │   ├── Generates corrected SQL
   │   └── Retries execution (up to 3 attempts)
   │
   └────┬────┘
        ▼
Results Returned to User
        │
        ▼
Representative Outputs Saved
```

---

## Pipeline Components

| Component | Purpose |
|----------|---------|
| **Database Loader** | Connects to the Chinook SQLite database and loads the schema. |
| **Schema Extraction** | Extracts tables, columns, and relationships to provide context for SQL generation. |
| **Prompt Builder** | Combines the user question with the database schema into a structured prompt. |
| **GPT-4o-mini** | Generates SQL queries from natural language prompts. |
| **SQL Safety Module** | Validates generated SQL before execution to prevent unsafe or invalid statements. |
| **SQLite Engine** | Executes validated SQL against the Chinook database. |
| **Self-Correction Loop** | Repairs failed SQL queries by using the returned database error message to generate a corrected query. |
| **Output Generator** | Displays query results and saves representative outputs for evaluation. |

---

## Technology Stack

| Layer | Technology | Purpose |
|------|------------|---------|
| **Programming Language** | Python | Core application logic |
| **LLM** | OpenAI GPT-4o-mini | Natural language to SQL generation |
| **Database** | SQLite | Stores the Chinook sample database |
| **Dataset** | Chinook | Digital music store database used for testing |
| **Prompt Engineering** | Custom prompt templates | Creates schema-aware prompts |
| **Validation** | SQL Safety Module | Verifies generated SQL before execution |
| **Configuration** | python-dotenv + YAML | Loads API keys and application settings |
| **Environment** | Virtual Environment + requirements.txt | Reproducible Python environment |

---

## 6. Running the Application

After completing the installation and configuration steps, execute the application from the project root directory.

```bash
python -m src.model_runner
```

Running this command automatically performs the following steps:

1. Connects to the Chinook SQLite database.
2. Extracts the complete database schema.
3. Creates a schema-aware prompt using the user's question.
4. Sends the prompt to GPT-4o-mini.
5. Generates an SQL query.
6. Validates the SQL query using the SQL Safety module.
7. Executes the SQL query against the SQLite database.
8. If execution fails, automatically enters the self-correction loop and retries the query (up to three attempts).
9. Returns the final results and saves representative outputs to the `outputs/` directory.

---

## Running with Docker

For a fully reproducible environment, the project can also be run in a Docker container instead of a local virtual environment.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- A `.env` file in the project root containing your OpenAI API key (see Section 3 above)

### Build the image

```bash
docker build -t text-to-sql-assistant .
```

### Run the container

```bash
docker run --env-file .env text-to-sql-assistant
```

This runs the same end-to-end pipeline as `python -m src.model_runner`, using the Docker image's own isolated Python environment. Results are saved inside the container to `outputs/`, matching the local run's behavior.

**Note:** The Docker build uses `requirements-docker.txt`, a minimal dependency list containing only the packages the application needs to run (`openai`, `python-dotenv`, `PyYAML`). This is separate from the full `requirements.txt`, which includes local development tools (Jupyter, LangChain, etc.) not needed inside the container.

---

## Example Questions

The application can answer natural language questions such as:

```text
Which artist has the most albums?

What are the top 5 genres by number of tracks?

How many customers are from the USA?

Which customer has spent the most money?

Which playlist contains the most tracks?
```

---

## Example Output

**Question**

```text
Which artist has the most albums?
```

**Generated SQL**

```sql
SELECT Artist.Name,
       COUNT(Album.AlbumId) AS AlbumCount
FROM Artist
JOIN Album
    ON Artist.ArtistId = Album.ArtistId
GROUP BY Artist.ArtistId
ORDER BY AlbumCount DESC
LIMIT 1;
```

**Result**

```text
Iron Maiden — 21 albums
```

---

## Self-Correction Example

If an invalid SQL query is generated, the application automatically retries after receiving the SQLite error message.

**Attempt 1**

```text
Error:
no such table: ArtistTable
```

The error is sent back to GPT-4o-mini along with the original question and generated SQL.

The model generates a corrected query.

```sql
SELECT Artist.Name,
       COUNT(Album.AlbumId)
FROM Artist
JOIN Album
ON Artist.ArtistId = Album.ArtistId
GROUP BY Artist.ArtistId
ORDER BY COUNT(Album.AlbumId) DESC
LIMIT 1;
```

The corrected query is executed automatically.

```text
SQL executed successfully on Attempt 2.

Result:
Iron Maiden — 21 albums
```

This self-correction mechanism improves reliability by allowing the application to repair SQL generation errors before returning a response to the user.

---

## Representative Outputs

Representative outputs generated during testing are saved in the `outputs/` directory.

Example:

```text
outputs/
├── sample_results.txt
└── README.md
```

These outputs demonstrate the application's ability to answer a variety of Text-to-SQL questions and serve as examples for evaluation and future development.

## 7. Evaluation Summary

The Text-to-SQL Assistant was evaluated using **20 benchmark questions** covering a variety of SQL tasks, including record retrieval, filtering, aggregation, sorting, ranking, and multi-table joins. The evaluation framework is implemented in `experiments/evaluation.ipynb` and was inspired by established Text-to-SQL benchmarks such as **Spider** and **BIRD**.

---

## Overall Performance

The application correctly answered **19 out of 20** benchmark questions, achieving an overall accuracy of **95.00%**.

```text
===========================================
Correct Answers: 19/20
Accuracy: 95.00%
===========================================
```

---

## Evaluation Results

| # | Question | Result | Correct |
|---:|----------|--------|:-------:|
| 1 | How many customers are in the database? | 59 | ✅ |
| 2 | How many music genres are available? | 25 | ✅ |
| 3 | Which country has the most customers? | USA (13) | ✅ |
| 4 | Which artist has released the most albums? | Iron Maiden (21) | ✅ |
| 5 | How many invoices are in the database? | 412 | ✅ |
| 6 | What are the five longest tracks? | Occupation / Precipice, Through a Looking Glass, and others | ✅ |
| 7 | How many employees are in the database? | 8 | ✅ |
| 8 | List all customers who live in Brazil. | Five customers returned | ✅ |
| 9 | Which employee supports the most customers? | Jane Peacock (21 customers) | ❌* |
| 10 | Which customer has spent the most money? | Customer #6 ($49.62) | ✅ |
| 11 | Which music genre has generated the highest revenue? | Rock ($826.65) | ✅ |
| 12 | What is the average invoice total? | $5.65 | ✅ |
| 13 | Which billing country generated the highest sales? | USA ($523.06) | ✅ |
| 14 | Which playlist contains the most tracks? | Playlist #1 (3,290 tracks) | ✅ |
| 15 | Which media type contains the most tracks? | MPEG Audio File (3,034 tracks) | ✅ |
| 16 | Which artist has the most tracks? | Iron Maiden (213 tracks) | ✅ |
| 17 | How many customers have never placed an order? | 0 | ✅ |
| 18 | Which country has the highest average invoice total?  | Chile ($6.66) | ✅ |
| 19 | What are the top five countries by total sales revenue?  | USA, Canada, France, Brazil, Germany | ✅ |
| 20 | Which customer placed the largest single order?  | Helena Holý ($25.86) | ✅ |

> **\*** Question 9 was marked incorrect because the evaluation script compared the output using an exact string match. The generated SQL correctly identified **Jane Peacock** as the employee supporting **21 customers**, but the formatting of the returned result differed from the expected output.
> The single reported failure was **not caused by incorrect SQL generation**.
> This discrepancy reflects a limitation of the evaluation script rather than a failure of the Text-to-SQL pipeline itself.
---

## Performance Analysis

The evaluation demonstrates that the pipeline successfully handles a wide range of SQL operations, including:

- Basic record retrieval
- Conditional filtering
- Aggregate functions (`COUNT`, `SUM`, `AVG`)
- Sorting and ordering
- Multi-table joins
- Ranking and Top-*N* queries

An overall accuracy of **95%** indicates that the application performs reliably across representative Text-to-SQL tasks using the Chinook database.
---

## 8. Model Selection

Three models were compared during development:

- OpenAI GPT-4o-mini (primary)
- Qwen2.5-7B-Instruct (open-source alternative, via HuggingFace)
- SQLCoder-7B (SQL-specialized alternative, tested live on Northeastern's GPU cluster)

After experimentation, **OpenAI GPT-4o-mini** was selected as the primary model for the application.

---

## Why GPT-4o-mini?

GPT-4o-mini provided the best balance of:

- SQL generation accuracy
- Response speed
- Cost efficiency
- Ease of deployment
- Reliability
- Simple API integration

Unlike locally hosted models, GPT-4o-mini required no GPU resources or additional infrastructure, allowing every team member to run the project using the same environment.

---

## Generation Settings

The application generates SQL using:

```text
temperature = 0
```

Using a temperature of **0** produces deterministic outputs, reducing randomness and improving the consistency of generated SQL queries across repeated executions.

---

## Alternative Models

Several alternative models were evaluated during development.

### SQLCoder

SQLCoder produced strong SQL queries but required significantly more computational resources and was slower to integrate into the overall pipeline.

### Qwen2.5-7B-Instruct

Qwen matched GPT-4o-mini's accuracy on our test questions (3/3, no self-correction needed) and is free to run via HuggingFace's Inference API. It was not selected as primary due to GPT-4o-mini's existing integration and paid-API reliability.

For the scope of this project, GPT-4o-mini provided the best combination of simplicity, reliability, and accuracy.

---

## 9. Future Improvements

Possible future enhancements include:

- Develop a Streamlit web interface for interactive user queries.
- Support multiple relational database systems beyond SQLite.
- Improve SQL safety validation using abstract syntax tree (AST) parsing.
- Expand benchmark testing with larger Text-to-SQL datasets.
- Add support for database visualization and schema exploration.
- Implement conversation memory for multi-turn database interactions.
- Integrate additional open-source LLMs for side-by-side model comparison.

---

## 10. License

This project is licensed under the **MIT License**.

You are free to use, modify, distribute, and build upon this project, provided that the original copyright notice and license are included.

For complete licensing terms, see the accompanying **LICENSE** file.

---

## References

1. Yu, T., Zhang, R., Yang, K., et al. (2018). *Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Tasks.* Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing (EMNLP).

2. Li, J., et al. (2024). *Can LLM Already Serve as a Database Interface? A Big Bench for Large-Scale Database Grounded Text-to-SQL.* Proceedings of the VLDB Endowment (VLDB 2024).

3. Rocha, L. *Chinook Database.* https://github.com/lerocha/chinook-database

4. OpenAI. *OpenAI API Documentation.* https://platform.openai.com/docs

5. Python Software Foundation. *python-dotenv Documentation.* https://pypi.org/project/python-dotenv/

---

## Acknowledgments

This project was developed as part of a Generative AI coursework project (**Group 02**). The work demonstrates the practical application of Large Language Models for natural language interfaces to relational databases, combining prompt engineering, schema-aware context generation, SQL validation, and iterative self-correction into a lightweight Text-to-SQL system.