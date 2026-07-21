"""
Safety scrubber for LLM generated SQL. The pipeline only needs to answer questions, so the only questions that should reach the database are read only such as SELECT statements. Everything else such as DELETE, INSERT, UPDATE, DROP, etc. should be denied here before it reaches teh cursor.execute().

Call is_safe_sql() on every SQL string immediately before execution.
"""

import re

FORBIDDEN_KEYWORDS = [
    "DELETE", "DROP", "UPDATE", "INSERT", "ALTER", "TRUNCATE",
    "REPLACE", "CREATE", "ATTACH", "DETACH", "PRAGMA", "VACUUM",
    "GRANT", "REVOKE", "REINDEX", "ANALYZE",
]
 
 
class UnsafeSQLError(Exception):
    """Raised when generated SQL fails the safety scrubber."""
    pass
 
 
def is_safe_sql(sql_query: str):
    """
    Checks that sql_query is a single, read-only SELECT statement.
 
    Returns:
        (is_safe: bool, reason: str)
    """
    if not sql_query or not sql_query.strip():
        return False, "Empty query"
 
    # Strip comments first, so a keyword can't be hidden after a
    # "--" or inside a "/* ... */" block.
    no_comments = re.sub(r"--.*?$", "", sql_query, flags=re.MULTILINE)
    no_comments = re.sub(r"/\*.*?\*/", "", no_comments, flags=re.DOTALL)
 
    # Reject stacked statements like "SELECT 1; DROP TABLE Artist;".
    # Only a single trailing semicolon is tolerated.
    stripped = no_comments.strip().rstrip(";")
    if ";" in stripped:
        return False, "Multiple SQL statements are not allowed"
 
    # Allow-list: query must start with SELECT (or WITH for a CTE
    # that ultimately SELECTs). Anything else is refused immediately.
    first_word_match = re.match(r"\s*(\w+)", stripped)
    first_word = first_word_match.group(1).upper() if first_word_match else ""
    if first_word not in ("SELECT", "WITH"):
        return False, f"Only SELECT queries are allowed (got '{first_word}')"
 
    # Backup block-list: forbidden keywords anywhere, matched as whole
    # words so a column like "UpdatedAt" doesn't false-positive.
    upper_sql = stripped.upper()
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", upper_sql):
            return False, f"Forbidden keyword detected: {keyword}"
 
    return True, "OK"
 
 
def assert_safe_sql(sql_query: str):
    """Same check as is_safe_sql(), but raises UnsafeSQLError on failure.
    Convenient when you want a hard stop instead of an (is_safe, reason) tuple.
    """
    safe, reason = is_safe_sql(sql_query)
    if not safe:
        raise UnsafeSQLError(f"Blocked unsafe SQL ({reason}): {sql_query}")
 