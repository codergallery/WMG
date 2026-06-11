# Day-1 (31-05-26)
## Github
### 1. CVCSs vs DVCSs
- CVSC stores file at one central server, DVCS stores file at multiple client systems.
- In CVCS client only has the **most recent copy** of the project, history is only stored on the central server, while in DVCS every client has the **full history** of the repo.

## Learnings

**Git & Version Control**
- CVCS stores files on one central server — clients only have the most recent copy, full history lives on the server
- DVCS stores full history on every client system — no single point of failure
- Git is a DVCS — every clone is a complete backup of the entire project history


# Day-2 (01-06-26)
## B. LLM Integration
### 1. Basic code
```python
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# client = genai.Client(api_key= "API_KEY")
client = genai.Client(api_key = gemini_api_key)

response = client.models.generate_content(
    model = "gemini-2.5-flash", 
    contents = "What is your opinion on learning by building? Give a brief overview in 50 words"
)

print(response.text)

# stream response

response = client.models.generate_content_stream(
    model = 'gemini-2.5-flash', 
    contents = "In users opinion, does free tier of Gemini API provide enough tokens for a small, one user personal project? Answer in 100 words!"
)

for chunk in response:
    print(chunk.text, end="", flush=False)
```
- *generate_content* gives the result when the whole content has been generated!
- *generate_content_stream* gives results as the content is being generated, doesn't wait for full content!  
We use loops in this scenario to print the result as it is being generated. 

## Learnings

**Gemini API & LLM Integration**
- Connected to Gemini API using `google-generativeai` — loaded API key from `.env` using `os.getenv()`
- Explicit is better than implicit — pass the API key directly to the client instead of relying on environment auto-detection
- `generate_content()` — waits for the full response before returning
- `generate_content_stream()` — returns chunks as they are generated; use a loop to print in real time
- Never hardcode API keys — always use `.env` and `.gitignore`; leaked keys must be revoked immediately

# Day-3 (02-02-26)
## JSON & Prompting
### 1. *JSON* - A standard format for data transfer
```python 
    import json

    # convert JSON data to python dictionary 
    dict_data = json.loads(json_data)

    # convert python dictionary to JSON data
    json_data = json.dumps(python_data)

    # JSON works with dictionary, lists, tuples, strings, integers, float, boolean, None
```
## 2. Prompting
- We created a prompt that reads user description, returns a JSON string; we convert that JSON string into python dictionary!  

```python
    import datetime

    # gives the current datetime
    current = datetime.datetime.now()
    
    # formatting the date and time
    current = current.strftime("%Y-%m-%d %H:%M")
```

## Learnings

**JSON & Python**
- JSON is a standard format for data transfer between systems
- `json.loads()` — converts a JSON string into a Python dictionary
- `json.dumps()` — converts a Python dictionary into a JSON string
- JSON is compatible with — `dict`, `list`, `tuple`, `str`, `int`, `float`, `bool`, `None`

**Prompting**
- Structured prompts can instruct an LLM to return JSON directly — parseable by Python without extra processing
- LLM responses may contain markdown artifacts like ` ```json ` — always clean before parsing

**datetime**
- `datetime.datetime.now()` — returns current date and time
- `strftime("%Y-%m-%d %H:%M")` — formats datetime into a readable string

# Day-4 (06-06-26)
## Database
### 1. Database Design  

| Expense ID | Items | Category | Amount | Date | Time |Description |      
| ---------- | ----- | -------- | ------ | ---- | ---- | ---------- |
|    1      | Maggi & Chai| Food | 40  | 2026-06-06 | 08:43 | Bought Maggi & Chai for 40 rupees|

### 2. Datatypes in SQLite
1. Expense ID - ***INTEGER PRIMARY KEY AUTOINCREMENT***
2. Items - TEXT 
3. Category - TEXT
4. Amount - ***REAL  NOT NULL***
5. Date - ***Stored as TEXT, worked using date(), strftime() functions***
6. Time - ***Stored as TEXT, worked using date(), strftime() functions***
7. Description - TEXT

- ***INTEGER PRIMARY KEY AUTOINCREMENT*** - The *AUTOINCREMENT* keyword automatically increases the count of that column by one and ensures that the database doesn't reuse the IDs of deleted rows, i.e, every ID must be strictly unique! 

- ***REAL NOT NULL*** - The *NOT NULL* keyword ensures that no rows are inserted with Empty/NULL values, i.e, in our case every row has a value for amount column.

### 3. SQL Concepts
##### 1. *CREATE TABLE* - Used to create a new table!
```SQL
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL,
    stock_quantity INTEGER
); 
```
- *IF NOT EXISTS* prevents from throwing an error if the table already exists! 

##### 2. *INSERT INTO* - Used to insert rows into existing tables!
```SQL
INSERT INTO products (column1, column2, column3)
VALUES (value1, value2, value3)
```
```
NOTES: 
    1. Text values must be enclosed inside single quotes. ('Macbook')
    2. Values must be in the order of the columns.
    3. Skip AUTOINCREMENT columns.
```

##### 3. *SELECT* - Used to pull out the data from database tables to read.  
```SQL
SELECT column1, column2 FROM table_name -- fetch the required columns from the table

SELECT * FROM table_name -- fetch all columns from the table 
```

##### 4. *WHERE* - Used to filter values from a table. 

```SQL
SELECT name FROM products -- only show the name column
WHERE name = 'Wireless mouse' -- 'wireless mouse' works too because SQL is case-insensitive  
-- '=' looks for exact matches 
```

```
NOTES:
    1. WHERE supports: = , != , > , < , >= , <=
    2. Combining conditions: AND (both True), OR(at least one True), NOT (reverse the condition)
    3. Shortcuts: 
        a. BETWEEN - Used to filter a range of numbers or dates
        b. IN - Match a specific value inside a specific list
        c. IS NULL / IS NOT NULL - Checks for empty of missing data  
```

```SQL
SELECT name FROM products 
WHERE price BETWEEN 20.00 AND 100.00

SELECT price FROM products 
WHERE name in ('Wireless Mouse', 'Keyboard')

SELECT * FROM products
WHERE stock_quantity IS NOT NULL
```

##### 5. *ORDER BY* - Used to sort the table based on specific columns

```SQL
SELECT * FROM products
ORDER BY price DESC -- sorts the table from most expensive to least expensive

-- ASC: Ascending (default), DESC: Descending
-- NULL: NULL is treated as smaller than any number, i.e, in ASC it will be at top while in DESC it will be at bottom

SELECT * FROM products
ORDER BY price ASC, name DESC -- we can sort by multiple columns, the secondary columns work as tie breaker

SELECT * FROM products 
WHERE price BETWEEN 20.00 AND 100.00
ORDER BY price DESC -- when filtering and sorting in the same query, WHERE always comes before ORDER BY
```

##### 6. *UPDATE* - Used to update the values of columns in existing data

***CAUTION*** - Never forget the **WHERE** when updating the value; without the **WHERE** filter it will update values for all rows

```SQL
UPDATE products
SET price = 79.99, stock_quantity = 80 -- columns whose values need to be updated
WHERE name = 'Mechanical Keyboard' -- important WHERE filter
```

##### 7. *DELETE* - Used to delete rows from a database table.

***CAUTION*** - Just like *UPDATE*, using **DELETE** without **WHERE** condition will delete **all rows**, leaving an empty structure.

```SQL
DELETE FROM products
WHERE product_id = 3 -- delete single row

DELETE FROM products
WHERE price < 16.00 -- delete multiple rows at once
```
### 4. SQLite Specific Concepts

##### 1. *Type Affinity*:
-  This means that in SQLite columns don't have a rigid datatype, they have a prefered one chosen through keywords we use while creating table using `CREATE TABLE*`. 
- It tries to convert the entered data into the specified data type of the column; if not possible then instead of throwing an error and crashing the whole program it stores the data as it is. 

##### 2. *Transactions (Commit and Rollback)*:
- In SQLite, transactions are like safe`UPDATE``INSERT`to the database without the worry of losing the data due to any`UPDATE``INSERT`transaction begins with `BEGIN TRANSACTION` or just `BEGIN` and ends with `COMMIT`. Between `BEGIN` and `COMMIT` whatever operations are performed are stored in a temporary journal file, it is only after `COMMIT` that these changes are written to the disk file.
- **ROLLBACK** command is used to undo the changes and go back to the state of `BEGIN`.
- `UPDATE` and `INSERT` commands are mini transactions in themselves, i.e, they can be rollbacked. 
- To increase performance time, group multiple statements inside a single `BEGIN` and `COMMIT` block. (File is opened and closed once instead of every time)

##### 3. *cursor.lastrowid*:
- Gives the *primary key* or hidden `row_id` of the last inserted row in the table. 
- The last *primary key* is stored in a temporary location and fetched using `cursor.lastrowid`.

##### 4. sqlite3.Row
- By default *sqlite3* returns rows as tuples, to convert it into dictionary we use `sqlite3.Row`.
- This dictionary is just read-only, to make changes we need to use the `UPDATE` command.

### 5. Python sqlite3

##### 1. *Connection*:
```python
import sqlite3

# conn = sqlite3.connect('expenses.db')
# opens the file, or creates one if it doesn't exist

# better approach for creating a connection using with
with sqlite3.connect('expense.db') as conn:
    print("Connected")
# with acts as a context manager, manages transactions by committing them if the block finishes successfully or rolling them back if an error occurs
# unlike working with text files, with doesn't automatically closes the connection
```
##### 2. *Cursor* and *execute*
```python
import sqlite3

with sqlite3.connect('expenses.db') as conn:
    cursor = conn.cursor()
# cursor is the one talking to the database, it executes the queries

# execute is used to run sql commands
cursor.execute(sqlcommand)
```

##### 3. *fetchall* and *fetchnone*
```python
import sqlite3

with sqlite3.connect('expense.db') as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    # fetchall - returns all rows as tuples
    for row in cursor.fetchall():
        print(row) # prints each row one by one

    # fetchone() - returns the next row, or NONE if it doesn't exist
    cursor.fetchone()
```

##### 4. *IntegrityError* - Happens when we try to bypass the constraints of a given column
```python 
import sqlite3

with sqlite3.connect('expense.db') as conn:
    cursor = conn.cursor()

    try:
        cursor.execute(...)
    except sqlite3.IntegrityError:
        print("Invalid input")
```

```
NOTES: 
    1. cursor.execute() is designed to insert one row at a time, for multiple rows use executemany() instead of looping. Bcz looping will write multiple times, while executemany handles this efficiently. 
    student_list = 
    [
    ('Mayank', 20),
    ('Shambhavi', 19), 
    ('Shekhar', 18)
    ]

    cursor.executemany("INSERT INTO students(name, age) 
    VALUES (?, ?)", student_list)
```
## Docstrings
### 1. Google style doctrings

```python
def function_name(param1, param2):
    """
    One line summary of what the function does.

    Longer description if needed — explain any important
    behavior, edge cases, or context.

    Args:
        param1 (type): Description of param1.
        param2 (type): Description of param2.

    Returns:
        type: Description of what is returned.

    Raises:
        ErrorType: When and why this error occurs.
    """
```

```python 
# No arguments, no return values
def function_name():
    """
    One line summary of what the function does.

    Longer description if needed.
    """

# omit Args, Returns and Raises
```
## Learnings

**Database & SQL**
- Designed the expenses table schema — chose appropriate SQLite data types for each column
- `INTEGER PRIMARY KEY AUTOINCREMENT` — auto-assigns unique IDs, never reuses deleted row IDs
- `NOT NULL` — enforces that a column cannot be empty on insert
- SQLite stores dates and times as `TEXT` — no native date type
- Core SQL commands — `CREATE TABLE`, `INSERT INTO`, `SELECT`, `WHERE`, `ORDER BY`, `UPDATE`, `DELETE`
- `UPDATE` and `DELETE` without `WHERE` affect all rows — always filter
- SQLite type affinity — columns have preferred types, not strict ones; stores data as-is if conversion fails
- Transactions — changes between `BEGIN` and `COMMIT` are written to a temp journal, not to disk until `COMMIT`; `ROLLBACK` undoes everything back to `BEGIN`
- `cursor.lastrowid` — fetches the primary key of the last inserted row
- `sqlite3.Row` — converts default tuple rows into named, dict-like objects; read-only

**Python sqlite3**
- `with sqlite3.connect()` — context manager that auto-commits or rolls back; does not auto-close the connection
- `cursor` — the object that executes SQL queries against the database
- `fetchall()` — returns all rows; `fetchone()` — returns next row or `None`
- `IntegrityError` — raised when a constraint like `NOT NULL` is violated
- `executemany()` — inserts multiple rows efficiently instead of looping `execute()`

**Docstrings**
- Google style is the industry standard for most Python projects
- Sections — summary line, `Args`, `Returns`, `Raises`; omit sections that don't apply
- `Args: None` and `Returns: None` are not valid Google style — omit the section entirely instead