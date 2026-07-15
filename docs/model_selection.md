# Model Selection & Literature Review

## 1. Objectives

Our Text-to-SQL pipeline needs a model that can:
- Read a database schema (table names, columns, data types) provided as context
- Translate a plain English question into valid SQLite syntax
- Work reliably within a self-correction retry loop (accept an error message and produce a corrected query)

The pipeline was initially built around **GPT-4o-mini**. This document evaluates that choice against two alternatives.

## 2. Models Considered

**GPT-4o-mini (primary)**: a general-purpose LLM accessed via OpenAI's API. Not SQL-specific, but broadly capable across many language tasks, including code and query generation. Already fully integrated into our pipeline, including the self-correction loop.

**Qwen2.5-7B-Instruct (alternative)**: an open-source, general-purpose instruction-tuned LLM, accessed via HuggingFace's free Inference API. Originally we intended to test Mistral-7B-Instruct, but it is no longer served as a chat-completion model on HuggingFace's free tier; we substituted Qwen2.5-7B-Instruct as a comparable open-source general model.

**SQLCoder (alternative)**: a family of models from Defog (7B, 15B, 34B, and 70B versions) fine-tuned specifically for text-to-SQL generation on top of base models like StarCoder and CodeLlama, rather than general-purpose language use. We first attempted to test the 7B version via HuggingFace's free Inference API; it returned a `model_not_supported` error, confirming it isn't served as a chat-completion model there. Since Northeastern's Explorer GPU cluster (Open OnDemand) was available, we ran the model directly instead of relying solely on a desk comparison.

Two things stood out during the live test that are worth documenting: SQLCoder did not produce usable output with the same generic prompt format used for GPT-4o-mini and Qwen. It requires its own documented prompt template (`### Task` / `### Database Schema` / `### Answer` sections) to generate anything at all. It also produced noticeably slower responses than the two API-based models, since inference ran on a single shared GPU rather than dedicated hosted infrastructure.

## 3. Comparison

| Model | Valid SQL? | Needed Correction? | Speed | Notes |
|---|---|---|---|---|
| GPT-4o-mini (primary) | Yes, 3/3 | No | Fast (few seconds/call) | Already integrated with self-correction loop; paid API |
| Qwen2.5-7B-Instruct | Yes, 3/3 | No | Fast (few seconds/call) | Free via HF Inference API; open-source, self-hostable if needed |
| SQLCoder-7B (live, GPU) | 2/3 on first try | Yes, 1 query (used PostgreSQL `ILIKE` instead of SQLite `LIKE`) | Slower (tens of seconds/call, single shared GPU) | Required its own prompt template; corrected successfully on first retry, reaching 3/3 |

All three questions tested were: *"Which artist has the most albums?"*, *"What are the top 5 genres by number of tracks?"*, and *"How many customers are from the USA?"* GPT-4o-mini and Qwen2.5-7B-Instruct produced valid, correct SQL on the first attempt for all three, with no self-correction needed. SQLCoder answered the first two questions correctly on its first attempt, but generated a PostgreSQL-specific `ILIKE` clause (invalid in SQLite) for the third question; feeding the error message back to the model in a single correction step produced valid SQLite syntax that returned the correct result. All three models reached 100% accuracy on this small test set once self-correction was accounted for.

## 4. Why We Chose GPT-4o-mini

GPT-4o-mini was our starting choice before this comparison, so this section revisits that decision.

With self-correction accounted for, all three models reached the same accuracy (3/3) on our test questions. Since accuracy alone doesn't separate them, the decision comes down to practical trade-offs:

- **Integration cost**: GPT-4o-mini is already fully wired into our pipeline, including the self-correction loop and error handling. Both alternatives matched, but neither exceeded, this result, so not enough justification to redo that integration work.
- **API reliability and infrastructure dependency**: GPT-4o-mini and Qwen are both accessed through simple, hosted API calls with no local hardware requirements. SQLCoder required a specialized prompt format and a GPU environment (Northeastern's Explorer cluster, in our case) to run at al. It's a real dependency that a general deployment wouldn't always have available. Testing alternatives also directly exposed a reliability risk with free hosted APIs: our originally planned model (Mistral-7B-Instruct) turned out not to be available as a chat-completion model on HuggingFace's free tier, and SQLCoder wasn't available there either.
- **Speed**: GPT-4o-mini and Qwen both responded in a few seconds via optimized hosted infrastructure. SQLCoder, run on a single shared GPU, took noticeably longer per query, which is a meaningful factor for an interactive application.
- **Setup complexity**: SQLCoder needed its own prompt template and a GPU-backed environment to work at all, whereas both general models worked with the same simple prompt structure already built into our pipeline.

In short: once self-correction is factored in, all three models are comparably accurate on this test set, but GPT-4o-mini and Qwen both offer simpler, faster, and more portable integration than SQLCoder, which depends on GPU access and a specialized prompt format to function. GPT-4o-mini's existing integration and stable paid-API reliability keep it as the right choice for this project's scope.

## 5. References

- Defog SQLCoder benchmark figures and model description: https://www.linkedin.com/posts/rishsriv_we-just-open-sourced-defog-sqlcoder-a-state-of-the-art-activity-7099661704879357952-HnI7
- SQLCoder-8B benchmark results: https://www.marktechpost.com/2024/05/15/defog-ai-introduces-llama-3-based-sqlcoder-8b-a-state-of-the-art-ai-model-for-generating-sql-queries-from-natural-language/
- SQLCoder fine-tuning methodology: https://defog.ai/blog/sqlcoder2-technical-details/
- Qwen2.5-7B-Instruct: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct
- HuggingFace Inference Providers documentation: https://huggingface.co/docs/inference-providers/tasks/chat-completion
- Live test notebooks: `experiments/model_test_mistral.ipynb` (Qwen), `experiments/model_test_sqlcoder.ipynb` (API attempt), `experiments/model_test_sqlcoder_gpu.ipynb` (live GPU test)
