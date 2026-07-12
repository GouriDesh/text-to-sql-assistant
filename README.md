# text-to-sql-assistant
A natural language to SQL query assistant powered by LangChain and OpenAI. This assistant will help translate plain English Questions into optimized executable SQL queries, run them against the provided database, and return clear conversational answers. 

---
## 1. Project Overview & Architecture
This project bridges the gap between complex relational databases and non-technical individuals. Instead of writing raw SQL code, users can query with plain English  and receive a direct answer drawn from the relational database. 
### Core Features
* **Natural Language Parsing:** Leverage Generative AI models to interpret user's queries and dynamically map requests to underlying database schemas
* **Automated SQL Generation:** Constructs accurate SQL statements
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

### Installation Steps (MacOS)
1.**Terminal Focus**
```bash
   cd ~/Desktop
```
2.**Clone the project repository**
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
8.**Configure OpenAI API Key**
```bash
OPENAI_API_KEY=your_actual_api_key_here
```
9. **Launch Notebook**
```bash
jupyter notebook
```