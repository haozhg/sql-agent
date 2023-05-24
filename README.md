## SQL Agent
This repo is a fast prototype of SQL Agent based on `langchain`. References
- https://python.langchain.com/en/latest/modules/chains/examples/sqlite.html
- https://python.langchain.com/en/latest/modules/chains/examples/sqlite.html

### Data
I tried to find public datasets with 400+ columns online, but given the time limit, the best I can find is [FIFA 22 complete player dataset](https://www.kaggle.com/datasets/stefanoleone992/fifa-22-complete-player-dataset?select=players_22.csv), which has 110 columns.

Here are the one-time set up steps needed to generate `fifa22.db` (sqlite db file). I have already done it, so you can skip this part, I document the steps here in case you wanna to reproduce it.

- Download data from above link
- unzip it
- move `archive/players_22.csv` to `fifa22.csv`
- `pip install csv-to-sqlite` and `ls fifa22.csv | csv-to-sqlite -o fifa22.db`

### Start SQL Agent
```
# create venv
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# get your OpenAI API key
# https://platform.openai.com/account/api-keys
export OPENAI_API_KEY='your_openai_api_key'

# start agent
python agent.py
```

### Examples
Question: find the total number of columns in fifa table?
```
Thought: I should check the schema of the fifa table to see how many columns it has.
Action: schema_sql_db
Action Input: "fifa"
Thought: The schema shows that there are 97 columns in the fifa table.
Final Answer: 97
```

Question: find the total number of rows in fifa table?
```
Thought: I should query the database to get the total number of rows in the fifa table.
Action: query_sql_db
Action Input: SELECT COUNT(*) FROM fifa
Observation: [(19239,)]
Thought: I now know the final answer
Final Answer: 19239
```

Question: list the number of fifa players per country
```
Thought: I should query the database to get the number of fifa players per country
Action: query_sql_db
Action Input: SELECT nationality_name, COUNT(*) AS num_players FROM fifa GROUP BY nationality_name ORDER BY num_players DESC LIMIT 10
Observation: [('England', 1719), ('Germany', 1214), ('Spain', 1086), ('France', 980), ('Argentina', 960), ('Brazil', 897), ('Japan', 546), ('Netherlands', 439), ('United States', 413), ('Poland', 403)]
Thought: I now know the final answer
Final Answer: The top 10 countries with the most FIFA players are England (1719), Germany (1214), Spain (1086), France (980), Argentina (960), Brazil (897), Japan (546), Netherlands (439), United States (413), and Poland (403).
```

Question: what's the distribution of player_positions in fifa table?
```
Thought: I should query the database to get the distribution of player_positions.
Action: query_sql_db
Action Input: SELECT player_positions, COUNT(*) FROM fifa GROUP BY player_positions ORDER BY COUNT(*) DESC LIMIT 10
Observation: [('CB', 2423), ('GK', 2132), ('ST', 1770), ('CDM, CM', 953), ('CM', 726), ('CM, CDM', 687), ('LB', 616), ('RB', 576), ('CB, RB', 295), ('CDM', 294)]
Thought: I now know the final answer
Final Answer: The most common player positions in the fifa table are CB (2423), GK (2132), ST (1770), CDM, CM (953), CM (726), CM, CDM (687), LB (616), RB (576), CB, RB (295), and CDM (294).
```

Question: what's the average wage_eur in the fifa table?
```
Thought: I should query the database to get the average wage_eur in the fifa table.
Action: query_sql_db
Action Input: SELECT AVG(wage_eur) FROM fifa
Observation: [(8989.396538281615,)]
Thought: I now know the final answer
Final Answer: The average wage_eur in the fifa table is 8989.396538281615.
```

Question: what's the mean and std of `age` in the `fifa` table?
```

```

Question: what's the mean, std, min, 25th percentile, medium, 75th percentile and max of `age` in the fifa table?
```
openai.error.InvalidRequestError: This model's maximum context length is 4097 tokens, however you requested 4201 tokens (3945 in your prompt; 256 for the completion). Please reduce your prompt; or completion length.
```
=> In the case of tables with hundres of columns, we can run into context length limit problem when the query gets complex and longer. The max context length of `text-davinci-003` is `4097`.


`Change model to gpt-3.5-turbo`
Question: what's the mean, std, min, 25th percentile, medium, 75th percentile and max of `age` in the fifa table?
```
> Entering new AgentExecutor chain...
Action: list_tables_sql_db
Action Input: ""
Observation: fifa
Thought:I should construct a query to get the requested statistics for the age column in the fifa table.
Action: query_checker_sql_db
Action Input: "SELECT AVG(age), STDDEV(age), MIN(age), PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY age), MAX(age) FROM fifa"
Observation: The original query appears to be correct and does not contain any of the common mistakes listed. Therefore, the original query is:

SELECT AVG(age), STDDEV(age), MIN(age), PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY age), MAX(age) FROM fifa
Thought:I should execute the query to get the final answer.
Action: query_sql_db
Action Input: "SELECT AVG(age), STDDEV(age), MIN(age), PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY age), MAX(age) FROM fifa"
Observation: Error: (sqlite3.OperationalError) near "(": syntax error
[SQL: SELECT AVG(age), STDDEV(age), MIN(age), PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY age), MAX(age) FROM fifa]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
Thought:I need to rewrite the query to fix the syntax error.
Action: query_checker_sql_db
Action Input: "SELECT AVG(age), STDDEV(age), MIN(age), PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY age), MAX(age) FROM fifa"
Observation: The original query appears to be correct and does not contain any of the common mistakes listed. Therefore, the original query is:

SELECT AVG(age), STDDEV(age), MIN(age), PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY age), MAX(age) FROM fifa
Thought:I should execute the query again now that I have confirmed it is correct.
Action: query_sql_db
Action Input: "SELECT AVG(age), STDDEV(age), MIN(age), PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY age), MAX(age) FROM fifa"
Observation: Error: (sqlite3.OperationalError) near "(": syntax error
[SQL: SELECT AVG(age), STDDEV(age), MIN(age), PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY age), PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY age), MAX(age) FROM fifa]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
Thought:I am not sure why the query is still giving a syntax error. I should double check the syntax for the PERCENTILE_CONT function.
Action: query_checker_sql_db
Action Input: "SELECT PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY age) FROM fifa"
Observation: The query is not valid for SQLite as it does not support the PERCENTILE_CONT function.
```
Even after I change LLM to `GPT-3.5`, the context length issue disappears (even though the max context length of `GPT-3.5` is same as `GPT-3`), I think somehow GPT-3.5 does a better job at generating more concise prompts and SQL commands. Still I found that it produces syntax errors in SQL queries.

### SQL Table with Hundreds of Columns
Challenges
- LLM context length limit issue for SQL table with many columns (prompt too long)
- When the agent needs to query multiple columns to answer a question, it can make SQL syntax mistakes and lose track of context
- When the agents needs to join multiple tables to answer a question, it can make SQL syntax mistakes and lose track of context

Improvements
- Use LLM with larger context length. e.g, `GPT-4` can handle 25k tokens, and `Claude` can handle 100k tokens (just released in early May 2023)
- Fine-tune LLM (e.g., GPT-3, GPT-3.5) on question to SQL pairs dataset and then use it as backbone in SQL Agent -> this is to improve LLM's ability to convert natural question to valid and complex SQL quries
- Experiment with different prompt template. Even thought langchain provides default prompt template, but it may not be optimal, we can try different prompts which can improve LLM ability in understanding user questions expressed in daily plan language. E.g., you can refer to [ChatGPT Prompt Engineering for Developers by Andrew Ng](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/) (release earlier May 2023), https://www.awesomegptprompts.com/, https://github.com/f/awesome-chatgpt-prompts