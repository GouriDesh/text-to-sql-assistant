# src/model_runner.py

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

from src.data_loader import load_config, connect_db, get_schema_string
from utils.helpers import build_prompt, build_correction_prompt
from src.sql_safety import is_safe_sql


def get_sql_from_llm(client, model, prompt, temperature=0):
    """Send a prompt to the LLM and return the generated SQL query."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert SQL assistant. Return only valid SQL queries."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()


def run_sql_with_correction(cursor, client, model, schema_string, user_question, sql_query, max_retries=3):
    """Run SQL, asking the LLM to fix it on failure, up to max_retries times. Every query is checked by the safety scrubber before execution. A query blocked as unsafe is not sent to the LLM for correction as a destructive query is not a bug that needs fixing. The safety scrubber will refuse the query and stop it instead of looping. """
    attempt = 0
    while attempt < max_retries:
        safe, reason = is_safe_sql(sql_query)
        if not safe:
            print(f"BLOCKED: unsafe SQL rejected ({reason}): {sql_query}")
            return None, sql_query
        try:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            return results, sql_query
        except Exception as error:
            attempt += 1
            if attempt >= max_retries:
                return None, sql_query
            correction_prompt = build_correction_prompt(user_question, sql_query, str(error), schema_string)
            sql_query = get_sql_from_llm(client, model, correction_prompt)


def text_to_sql_pipeline(cursor, client, model, schema_string, user_question, max_retries=3):
    """Full pipeline: question -> prompt -> LLM -> SQL -> database -> result."""
    prompt = build_prompt(schema_string, user_question)
    sql_query = get_sql_from_llm(client, model, prompt)
    results, final_sql = run_sql_with_correction(
        cursor, client, model, schema_string, user_question, sql_query, max_retries
    )
    return {
        "question": user_question,
        "sql": final_sql,
        "results": results
    }


def main():
    load_dotenv()
    client = OpenAI()

    config = load_config()
    conn, cursor = connect_db(config["db_path"])
    schema_string = get_schema_string(cursor)

    sample_questions = [
        "Which artist has the most albums?",
        "What are the top 5 genres by number of tracks?",
        "How many customers are from the USA?",
        "Which employee supports the most customers?",
        "What is the total revenue in 2022?",
    ]

    os.makedirs("outputs", exist_ok=True)
    all_results = []

    for question in sample_questions:
        print(f"Running: {question}")
        result = text_to_sql_pipeline(
            cursor, client, config["model"], schema_string, question, config["max_retries"]
        )
        all_results.append(result)
        print(f"  -> {result['results']}")

    output_path = f"outputs/samples_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\nSaved {len(all_results)} results to {output_path}")


if __name__ == "__main__":
    main()
