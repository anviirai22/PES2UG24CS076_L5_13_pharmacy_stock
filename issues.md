# Static Code Analysis — Issues Report

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| SQL injection risk | Security — Medium | 21 | The patient lookup query inserts user input directly into SQL, which could allow a crafted input to alter the query. | Replace string interpolation with a parameterized SQL query. |
| Unsafe medicine dispensing | Functional / Data Integrity — High | 29–39, 70–73 | The program permits dispensing more units than available and accepts negative stock additions, resulting in invalid stock values. | Validate positive quantities and check stock availability before dispensing. |
| Allergy check is case-sensitive | Functional / Safety — High | 31–33 | A medicine name such as `Penicillin` does not match the stored allergy `penicillin`, potentially allowing an unsafe dispense. | Normalize names before checking allergies and use explicit matching logic. |
| Broad exception handling | Reliability / Code Quality | 38, 58 | Bare `except` blocks hide unexpected errors and make debugging difficult. | Catch specific expected exceptions and handle invalid input or missing files deliberately. |
| Mutable default argument | Code Quality | 24 | `batch_log=[]` creates a shared mutable default that can retain data between calls. | Use `None` as the default and create a new list inside the function. |
| Unsafe file handling | Reliability / Code Quality | 50, 57 | Files are opened without context managers or explicit encoding, so resource cleanup and text encoding are not handled clearly. | Use `with open(..., encoding="utf-8")` and handle file errors appropriately. |
| Missing docstrings and style issues | Maintainability / Style | Multiple | Several functions lack docstrings; `printStock` does not follow snake_case naming, and lines/spacing violate style rules. | Add concise docstrings, rename the function, and format the code consistently. |
| Unused import | Code Quality | 3 | The `os` module is imported but never used. | Remove the unused import. |