Lab 5 — Reflection


1. Which issues were the easiest to fix, and which were the hardest? Why?

Problems like unused imports, lack of docstring, wrong names, line length, and style of file handling were the simplest problems to solve because they only needed some simple steps, like removing unused imports, creating docstrings, snake_casing names, and using context managers.

Problems like SQL injection problem and logical errors when dispensing medicine were the most challenging problems to solve. Such problems demanded knowledge on how user inputs affect queries to databases, how allergy testing works, and how not to dispense more medicine than what is available in stock.



2. Did the static analysis tools report any false positives? If so, describe one example.

False positives were not found in the results obtained by means of the use of Pylint, Bandit, or Flake8. The majority of the problems mentioned were valid and could be fixed with code modifications.

Nevertheless, the programs did not find all the functional errors. For instance, the program had an opportunity for stocks to be negative if more medicine is dispensed than the stock available. It was found out with manual testing.


3. How would you integrate static analysis tools into your actual software development workflow?

I would incorporate the use of Pylint, Bandit, and Flake8 in the development process such that they are run whenever there is any change made in the code. The developers could use the software tools locally before making any commits, or they could be incorporated into the continuous integration pipeline such that they check out automatically when there is a pull request.

Some critical security and code quality issues could be set up to automatically block a merge until these issues are fixed.


4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The code became more understandable and maintainable by implementing docstrings, following proper naming conventions, eliminating unnecessary imports, and improving file handling. The SQL statement was updated using parameters to avoid SQL injection. Medicine dispensing was further made reliable by implementing input validation and checking for stock, while the allergy check now becomes case-insensitive.

The Pylint score improved from 6.90/10 to 9.83/10. Bandit detected no problems in the last scan, and Flake8 found no style violations. Two Pylint warnings regarding the number of return statements remained. In general, the exercise demonstrates the efficiency of combining static analysis with manual testing and code review.