# text-to-sql-assistant
A natural language to SQL query assistant powered by LangChain and OpenAI. This assistant will help translate plain English Questions into optimized executable SQL queries, run them against the provided database, and return clear conversational answers. 

Built as a group project (Group 02) to explore practical, lightweight GenAI application development: prompt engineering, LLM API integration, schema-aware in-context learning, and agentic self-correction.

**Team:** Raquel Amarins, Patricia Atkinson, Gouri Deshpande, Tiffany Huynh

---
## 1. Project Overview & Architecture
This project bridges the gap between complex relational databases and non-technical individuals. Instead of writing raw SQL code, users can query with plain English  and receive a direct answer drawn from the relational database. 
### Core Features
- **Schema extraction** — reads the Chinook database structure (tables, columns, types) and formats it into a clean string for prompting.
* **Natural Language Parsing:** Leverage Generative AI models to interpret user's queries and dynamically map requests to underlying database schemas
* **Automated SQL Generation with Self Correction Loop:** Constructs accurate SQL statements with a build in self correction loop for errors which attempts to fix and retry the query (up to 3 attempts). This is a lightweight agentic behavior pattern..
* **Synthesis & Output:** Executes the commands against a read-only local database file and synthesizes into analytical text responses.

Example interactions this project targets:
- *"Which artist has the most albums?"*
- *"What are the top 5 genres by number of tracks?"*
- *"How many customers are from the USA?"*

### Technical Stack
* **Orchestration:** LangChain: Connects LLM, prompts, and databases
* **LLM Engine:** OpenAI GPT-4o-mini
* **Local Database:** SQLite + Chinook, representing a digital media store with artists, playlists, tracks, and other data tables.
* **Dataset:** [Chinook](https://github.com/lerocha/chinook-database), a well-known sample SQLite database representing a digital music store — 11 tables covering artists, albums, tracks, customers, invoices, employees, and more.
* **Enviornment Configuration:** 'python-dotenv' for isolating and securing private API credentials 

---
## 2. Repository Folder Structure

```
text-to-sql-assistant/
├── data/
│   └── Chinook_Sqlite.sqlite       # Local SQLite database (downloaded, not written by us)
├── configs/
│   └── model_config.yaml           # Centralized model and parameter configs
├── experiments/
│   ├── schema_extraction.ipynb     # Step 1: reads schema from the database
│   ├── core_pipeline.ipynb         # Step 2: prompt building, LLM call, SQL execution,
│   │                               #         self-correction loop (all added to this notebook)
│   └── evaluation.ipynb            # Step 3: runs the 20 benchmark questions
├── docs/
│   └── evaluation_results.md       # Recorded accuracy results from the benchmark run
├── .env                            # Your personal API key — NEVER committed (see Section 4)
├── utils/
│   └── helpers.py                  # Helper functions for prompt format, build, and corrections
├── .gitignore                      # Excludes .env, venv/, __pycache__, checkpoints, etc.
├── requirements.txt                # Pinned package versions for reproducibility
├── LICENSE                         # MIT License
└── README.md                       # You are here
```

> **Note:** `.env` is listed here to show where it lives, but it should never actually appear in the GitHub repo itself — it's excluded via `.gitignore` and exists only on each contributor's local machine.




---
## 3. Enviornment Set Up Guide
These steps get the project running from scratch on your machine. Follow the section for your operating system. Anywhere you see `your-api-key-here`, replace it with your own personal OpenAI API key.

### Prerequisites
* Windows or macOS
* Python 3.12+
* Git installed
* Jupyter Notebook, installed via pip (no separate install needed)
* An active OpenAI API Key with billing and usage credits configured

### 3.1 Windows (Using Git Bash)
Git Bash is recommended on Windows because the commands match Mac/Linux almost exactly.

```bash
# 1. Navigate to where you want the project folder to live
cd /c/Users/<your-username>/Documents

# 2. Clone the repository
git clone https://github.com/GouriDesh/text-to-sql-assistant.git
cd text-to-sql-assistant

# 3. Create the virtual environment
python -m venv venv

# 4. Activate it (note the Windows-specific path: Scripts, not bin)
source venv/Scripts/activate
# Your prompt should now show (venv) at the start

# 5. Upgrade pip, then install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 6. Register this venv as a Jupyter kernel (optional, but recommended)
python -m ipykernel install --user --name=venv --display-name "Python 3 (Project Venv)"

# 7. Create your local .env file (see Section 4 for what goes in it)
touch .env

# 8. Launch Jupyter
jupyter notebook
```

---

### 3.2 macOS

```bash
# 1. Navigate to where you want the project folder to live
cd ~/Documents

# 2. Clone the repository
git clone https://github.com/GouriDesh/text-to-sql-assistant.git
cd text-to-sql-assistant

# 3. Create the virtual environment
python3 -m venv venv

# 4. Activate it
source venv/bin/activate
# Your prompt should now show (venv) at the start

# 5. Upgrade pip, then install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 6. Register this venv as a Jupyter kernel (optional, but recommended)
python -m ipykernel install --user --name=venv --display-name "Python 3 (Project Venv)"

# 7. Create your local .env file (see Section 4 for what goes in it)
touch .env

# 8. Launch Jupyter
jupyter notebook
```

---

### 3.3 Linux

Identical to macOS:

```bash
cd ~/Documents
git clone https://github.com/GouriDesh/text-to-sql-assistant.git
cd text-to-sql-assistant

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name=venv --display-name "Python 3 (Project Venv)"

touch .env
jupyter notebook
```

---

### 3.4 Every session, going forward

Each time you sit down to work on the project (any OS), do this first:

```bash
cd text-to-sql-assistant     # go to the project folder
git pull                     # get your teammates' latest changes
source venv/Scripts/activate # Windows (Git Bash)
# or
source venv/bin/activate     # Mac/Linux
jupyter notebook
```

When you're done working, you can exit the virtual environment with:
```bash
deactivate
```

### 3.5 Downloading the database

If `data/Chinook_Sqlite.sqlite` isn't already in your cloned copy, download it from the official Chinook repo:

- Source: https://github.com/lerocha/chinook-database
- File needed: `Chinook_Sqlite.sqlite` (found under `ChinookDatabase/DataSources`)
- Place it in the `data/` folder at the project root.

### 3.6 Keeping requirements.txt up to date

If you install a new package, regenerate the file so teammates stay in sync:

```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update_requirements.txt"
git push
```

---

## 4. API Key Safety Practices
Your OpenAI API key is tied to your personal account and billing, treat it like a password.

**Ground Rules The Team Abides To:**

1. **Never commit `.env` to Git.** It's already excluded via `.gitignore` (generated from GitHub's Python template), so a normal `git add .` will not pick it up. Don't override this.
2. **Each teammate creates their own `.env` file locally** — do not share a single key across the team. Your `.env` should contain only:
   ```
   OPENAI_API_KEY=your-personal-key-here
   ```
3. **Never paste your key into code, notebooks, chats, or documentation.** If a key ever needs to be shared for debugging, share the *error*, not the key.
4. **Set a usage limit** in your OpenAI account (platform.openai.com → billing) so a bug can't run up unexpected charges.
5. **If a key is ever exposed** (accidentally committed, pasted somewhere public, etc.), go to platform.openai.com immediately, revoke or delete that key, and generate a new one. Then update your local `.env`.
6. **Double check before every push.** Run `git status` before `git add .` and confirm `.env` isn't listed as a tracked/staged file.


## 5. Architecture

This reflects what's actually implemented in the notebooks today 

```
User Question (plain English)
        │
        ▼
Schema Extraction  ──  reads Chinook via sqlite3 (PRAGMA table_info),
                        formats tables/columns into a prompt-ready string
        │
        ▼
Prompt Builder  ──  combines: schema string + formatting rules + user question
        │
        ▼
OpenAI GPT-4o-mini (temperature=0)  ──  returns a SQL query as plain text
        │
        ▼
SQL Execution on SQLite (Chinook)
        │
   ┌────┴────┐
   │         │
 Success   Failure
   │         │
   │         ▼
   │   Self-Correction Loop
   │   ──  sends failed SQL + exact error message back to the LLM
   │   ──  LLM returns a corrected query
   │   ──  retries execution (up to 3 attempts total)
   │         │
   └────┬────┘
        ▼
Result returned to the user
```

**Current tech stack:**

| Layer | Technology | Purpose |
|---|---|---|
| LLM | OpenAI GPT-4o-mini (`openai` Python SDK) | Converts natural language → SQL |
| Database | SQLite + Chinook | Stores and executes queries against sample data |
| Prompting | Custom Python functions (`build_prompt`, `build_correction_prompt`) | Injects schema + rules + question into the LLM call |
| Reliability | Custom retry loop (`run_sql_with_correction`) | Catches SQL errors and asks the LLM to self-correct |
| Config | `python-dotenv` | Loads the API key from `.env` without hardcoding it |
| Environment | `venv` + `requirements.txt` | Reproducible, isolated Python environment |

---

## 6. Usage Example

All current functionality runs inside `experiments/core_pipeline.ipynb` such as the schema loading, prompt building, LLM call, execution, and self-correction loop.

```python
# Test the updated pipeline with self-correction
text_to_sql_pipeline_v2("Which artist has the most albums?")
print()
text_to_sql_pipeline_v2("What are the top 5 genres by number of tracks?")
print()
text_to_sql_pipeline_v2("How many customers are from the USA?")
```

**Expected Execution Outcome**
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
Results: [(13,)]

```

**Example of self-correction kicking in** (when the LLM's first attempt fails):

```
Testing self-correction loop with a broken SQL query...
---
Attempt 1 failed: no such table: NonExistentTable
Asking LLM to fix the SQL...
Corrected SQL: SELECT Artist.Name, COUNT(Album.AlbumId) AS AlbumCount ...
SQL succeeded on attempt 2
Final results: [('Iron Maiden', 21)]
```

---

## 7. Evaluation Summary
An evaluation  (`experiments/evaluation.ipynb`) has been set up to test the pipeline against 20 benchmark questions varying across simple lookups, aggregations, and multi-table joins inspired by the Spider and BIRD textto SQL benchmarks.

### Result: 19 / 20 correct — 95.00% accuracy

```
==================================================
Correct Answers: 19/20
Accuracy: 95.00%
==================================================
```

**Full results:**

| # | Question | Generated result | Correct? |
|---|---|---|---|
| 1 | How many customers are in the database? | 59 | ✅ |
| 2 | How many music genres are available? | 25 | ✅ |
| 3 | Which country has the most customers? | USA (13) | ✅ |
| 4 | Which artist has released the most albums? | Iron Maiden (21) | ✅ |
| 5 | How many invoices are in the database? | 412 | ✅ |
| 6 | What are the five longest tracks? | Occupation / Precipice, Through a Looking Glass, +3 more | ✅ |
| 7 | How many employees are in the database? | 8 | ✅ |
| 8 | List all customers who live in Brazil. | 5 customers returned | ✅ |
| 9 | Which employee supports the most customers? | Jane Peacock (21 customers) | ❌* |
| 10 | Which customer has spent the most money? | Customer #6 — $49.62 | ✅ |
| 11 | Which music genre has generated the highest revenue? | Rock — $826.65 | ✅ |
| 12 | What is the average invoice total? | $5.65 | ✅ |
| 13 | Which billing country generated the highest sales? | USA — $523.06 | ✅ |
| 14 | Which playlist contains the most tracks? | Playlist #1 — 3,290 tracks | ✅ |
| 15 | Which media type contains the most tracks? | Media type #1 — 3,034 tracks | ✅ |
| 16 | Which artist has the most tracks? | Iron Maiden (213 tracks) | ✅ |
| 17 | How many customers have never placed an order? | 0 | ✅ |
| 18 | Which country has the highest average invoice total? | Chile — $6.66 | ✅ |
| 19 | What are the top five countries by total sales revenue? | USA, Canada, France, Brazil, Germany | ✅ |
| 20 | Which customer placed the largest single order? | Helena Holý — $25.86 | ✅ |

\* **Question 9 is a false negative, not a real failure.** The generated SQL returned the correct employee and count but the automated checked expected one exact substring however the results yield two separate fields. The pipeline itsef did not make a logic or SQL error


## 8. Model Selection Summary

The project proposal considered three options for the LLM layer:
- OpenAI GPT-4o-mini
- A LLaMA model
- An open-source, pretrained model from Hugging Face

**Decision: OpenAI GPT-4o-mini**, called directly via the `openai` Python SDK.

**Why:**

- Low cost per call and and fast response times, crucial for an interactive chat tool
- No need to manage or host model locally which keeps the team's set up lightweight across everyone's machines
- Stonger quality with SQL generation without the need to further fine tune
- `temperature=0` is used for all SQL generation calls to keep output deterministic and precise rather than creative.

## 9. License

This project is licensed under the **MIT License** — see the [`LICENSE`](LICENSE) file for full terms. In short: anyone is free to use, copy, modify, and distribute this code, including for commercial purposes, as long as the original copyright and license notice are included.


## References

1. Yu, T., et al. (2018). *Spider: A large-scale human-labeled dataset for complex and cross-domain semantic parsing and text-to-SQL task.* EMNLP 2018.
2. Li, J., et al. (2024). *Can LLM already serve as a database interface? A big bench for large-scale database grounded text-to-SQL.* VLDB 2024.
3. Rocha, L. *Chinook Database.* https://github.com/lerocha/chinook-database
