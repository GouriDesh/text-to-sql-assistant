# text-to-sql-assistant
A natural language to SQL query assistant powered by LangChain and OpenAI. This assistant will help translate plain English Questions into optimized executable SQL queries, run them against the provided database, and return clear conversational answers. 

---
## 1. Project Overview & Architecture
This project bridges the gap between complex relational databases and non-technical individuals. Instead of writing raw SQL code, users can query with plain English  and receive a direct answer drawn from the relational database. 
### Core Features
* **Natural Language Parsing: Leverage Generative AI models to interpret user's queries and dynamically map requests to underlying database schemas
* **Automated SQL Generation: Constructs accurate SQL statements
* ** Synthesis & Output: Executes the commands against a read-only local database file and synthesizes into analytical text responses.

### Technical Stack
* **Orchestration:** LangChain: Connects LLM, prompts, and databases
* **LLM Engine:** OpenAI GPT-4o-mini
* **Local Database:** SQLite + Chinook, representing a digital media store with artists, playlists, tracks, and other data tables.
* **Enviornment Configuration:** 'python-dotenv' for isolating and securing private API credentials 

---
## 2. Enviornment Set Up Guide

### Prerequisites

### Installation Steps

