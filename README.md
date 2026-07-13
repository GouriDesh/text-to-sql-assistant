# text-to-sql-assistant
A natural language to SQL query assistant powered by LangChain and OpenAI. This assistant will help translate plain English Questions into optimized executable SQL queries, run them against the provided database, and return clear conversational answers. 

---
## 1. Project Overview & Architecture
This project bridges the gap between complex relational databases and non-technical individuals. Instead of writing raw SQL code, users can query with plain English  and receive a direct answer drawn from the relational database. 
### Core Features
* **Natural Language Parsing:** Leverage Generative AI models to interpret user's queries and dynamically map requests to underlying database schemas
* **Automated SQL Generation with Self Correction Loop:** Constructs accurate SQL statements with a build in self correction loop for errors.
* **Synthesis & Output:** Executes the commands against a read-only local database file and synthesizes into analytical text responses.

### Technical Stack
* **Orchestration:** LangChain: Connects LLM, prompts, and databases
* **LLM Engine:** OpenAI GPT-4o-mini
* **Local Database:** SQLite + Chinook, representing a digital media store with artists, playlists, tracks, and other data tables.
* **Enviornment Configuration:** 'python-dotenv' for isolating and securing private API credentials 

---
## 2. Enviornment Set Up Guide
Follow this step by step guide to mirror the development enviornment and get the codebase running locally on your computer
### Prerequisites
* Windows or macOS
* Python 3.12+
* An active OpenAI API Key with usage credits

### Installation Steps 
0. **System of Choice**
MacOS users proceed by using Terminal. Windows users proceed by using Command Prompt or GitBash to run these commands
1. **Terminal Focus**
```bash
   cd ~/Desktop
```
2. **Clone the project repository**
```bash
   git clone https://github.com/GouriDesh/text-to-sql-assistant.git
   cd text-to-sql-assistant
```
3. **Configure Virtual Environment**
 ```bash
    python3 -m venv venv
```
4. **Activate Virtual Environment**
```bash
source venv/bin/activate
```
5. **Install Package Installer and Softwares**
```bash
pip install --upgrade pip
pip install openai langchain langchain-openai python-dotenv jupyter ipykernel
```
6. **Link Virtual Environment to Jupyter**
```bash
python -m ipykernel install --user --name=venv --display-name "Python 3 (Project Venv)"
```
7. **Create Enviornment Configuration File**
```bash
touch .env
```
8. **Configure OpenAI API Key**
```bash
OPENAI_API_KEY=your_actual_api_key_here
```
9. **Launch Notebook**
```bash
jupyter notebook
```
---
## 3.Architecture Design
The architecture leverages a modular framework built using LangChain
1. **User Input Query:** Receives raw conversational quertion from the developer interface.
2. **Schema Prompting:** The internal system will retrieve the targeted database (ie. tables, primary/foreign keys, data types) and inject it along a specialized system prompt.
3. **LLM Generation:** The LLM evaluates the context and structures and insolated SQL statement.
4. **Parsing & Safety Execution:** The system will extract the raw string back, scrubbing destructive or unauthorized clauses before passing clean text to the designated SQL engine.
[User Input] ──> [Schema Context + Prompt Wrapper] ──> [OpenAI LLM Engine] ──> [Safety Scrubber] ──> [Valid SQL Output]

---
## 4. Usage Examples
This repository includes interactive end-to-end execution pipeline featuring an automatic SQL self correction logic.

### Example

```python
# Test the updated pipeline with self-correction
text_to_sql_pipeline_v2("Which artist has the most albums?")
print()
text_to_sql_pipeline_v2("What are the top 5 genres by number of tracks?")
print()
text_to_sql_pipeline_v2("How many customers are from the USA?")
```
### Expected Execution Outcome
```text
Question: Which artist has the most albums?
---
Generated SQL: SELECT Artist.Name, COUNT(Album.AlbumId) AS AlbumCount
FROM Artist
JOIN Album ON Artist.ArtistId = Album.ArtistId
GROUP BY Artist.ArtistId
ORDER BY AlbumCount DESC
LIMIT 1;
---
Results: [('Iron Maiden', 21)]

Question: What are the top 5 genres by number of tracks?
---
Generated SQL: SELECT g.Name, COUNT(t.TrackId) AS TrackCount
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
GROUP BY g.GenreId
ORDER BY TrackCount DESC
LIMIT 5;
---
Results: [('Rock', 1297), ('Latin', 579), ('Metal', 374), ('Alternative & Punk', 332), ('Jazz', 130)]

Question: How many customers are from the USA?
---
Generated SQL: SELECT COUNT(*) FROM Customer WHERE Country = 'USA';
---

```