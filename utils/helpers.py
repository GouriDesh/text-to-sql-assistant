# CELL 2: Load Schema String
# Format schema as a clean string for the LLM prompt
def format_schema_for_prompt(schema):
    schema_str = ''
    for table, columns in schema.items():
        schema_str += f'Table: {table}\n'
        for col_name, col_type in columns:
            schema_str += f'  - {col_name} ({col_type})\n'
        schema_str += '\n'
    return schema_str


# CELL 3: Build the Prompt
def build_prompt(schema_string, user_question):
    prompt = f"""You are an expert SQL assistant.

You are given the following database schema:
{schema_string}

Write a valid SQLite SQL query to answer the following question:
{user_question}

Rules:
- Return ONLY the SQL query, nothing else
- Do not include any explanation or markdown
- Do not use ```sql or ``` in your response
- Make sure the query is valid SQLite syntax
"""
    return prompt


# CELL 7: Build the Correction Prompt
def build_correction_prompt(user_question, failed_sql, error_message, schema_string):
    prompt = f"""The following SQL query failed when run on a SQLite database:

{failed_sql}

Error message:
{error_message}

Here is the correct database schema:
{schema_string}

Please fix the SQL query to correctly answer the following question:
{user_question}

Rules:
- Return ONLY the corrected SQL query, nothing else
- Do not include any explanation or markdown
- Do not use ```sql or ``` in your response
- Make sure the query is valid SQLite syntax
- Only use table and column names that exist in the schema above
"""
    return prompt