## 1. Workflow
- [ ] Apply this checklist to the target file
- [ ] Make appropriate changes
- [ ] Summarize what the changes were

## 2. File Header
- [ ] Shebang present
- [ ] Module name + one‑line description
- [ ] Author is Pito Salas and Claude
- [ ] MIT license header

## 3. Imports
- [ ] All imports at top
- [ ] Absolute imports only
- [ ] No unused imports
- [ ] No ROS2 imports in library modules
- [ ] No wildcard imports
- [ ] Imports sorted (Ruff/isort)
- [ ] Dependencies declared in pyproject.toml

## 4. Style
- [ ] Double quotes
- [ ] No `from __future__ import annotations`
- [ ] No `Optional[X]` (use `X | None`)
- [ ] No underscore‑prefixed private names
- [ ] Line length ≤ 88 chars
- [ ] Identifiers ≤ 15 chars and intention‑revealing

## 5. Structure
- [ ] Functions/methods ≤ 50 lines
- [ ] File ≤ 300 lines
- [ ] One class per file
- [ ] No nested if/else deeper than 1
- [ ] No if with >3 branches
- [ ] No 1–2 line methods
- [ ] No simple wrappers
- [ ] No functions with >3 arguments
- [ ] No default parameters
- [ ] No single‑use temp variables

## 6. Documentation
- [ ] Public functions/classes have brief docstrings
- [ ] Complex functions include examples
- [ ] Comments explain WHY, not WHAT
- [ ] No task/fix references in comments

## 7. Type Safety
- [ ] Parameters annotated when non‑obvious
- [ ] Return types annotated
- [ ] Prefer simple types
- [ ] No `Any` unless unavoidable

## 8. Naming
- [ ] Boolean names use `is_`, `has_`, `can_`
- [ ] No single‑letter names except loop counters
- [ ] No _ prefix on private functions, methods and variables

## 9. Data & State
- [ ] No logic in `__init__` beyond assignment
- [ ] No import‑time side effects
- [ ] No in‑place mutation unless obvious
- [ ] Dataclasses use `default_factory`

## 10. Design
- [ ] No god methods
- [ ] No feature envy
- [ ] No data clumps
- [ ] Single responsibility per class
- [ ] Methods at same abstraction level
- [ ] Minimal public API
- [ ] Internal helpers separated
- [ ] Mutable state only when necessary
- [ ] No upward dependency violations

## 11. Schema Duplication
- [ ] No parallel dataclasses with repeated fields
- [ ] Tie dataclasses to code and to configuration yaml
- [ ] No hand‑transcribed schemas
- [ ] Adding a field requires ≤1 other file change

## 12. Error Handling
- [ ] No bare `except Exception`
- [ ] No silent swallowing
- [ ] No defensive coding for impossible cases
- [ ] Validation only at boundaries
- [ ] Use `logger.error`, not `print`
- [ ] Use context managers for cleanup
- [ ] Meaningful error messages

## 13. Performance & Optimization
- [ ] Prefer optimal big‑O algorithms
- [ ] Avoid unnecessary loops/allocations
- [ ] Use vectorization/parallelization when appropriate
- [ ] No redundant logic
- [ ] Code minimal and efficient

## 14. Python Best Practices
- [ ] Use `is` for None/True/False
- [ ] Use f‑strings
- [ ] Use comprehensions/generators
- [ ] Use `enumerate()`
- [ ] Use context managers for all resources

## 15. Tooling Standards
- [ ] Use `uv` for package management for non ROS tools
- [ ] Use `polars` (never pandas)

## 16. Data Science Rules
- [ ] Never ingest >10 rows during analysis
- [ ] Never print schema + row count together
- [ ] Use polars exclusively

## 17. Database Schema Quality
- [ ] No denormalization unless required
- [ ] Use correct SQL types (DATETIME/TIMESTAMP, ARRAY, etc.)
- [ ] Never store nested structures as TEXT

## 18. Security
- [ ] No secrets or credentials in code
- [ ] `.env` used for sensitive config
- [ ] `.env` in `.gitignore`
- [ ] Never log sensitive data
- [ ] Never print URLs with tokens

## 19. Test Coverage
- [ ] Every public method tested
- [ ] Edge cases covered
- [ ] Non‑obvious behavior tested
- [ ] Regression tests for fixed bugs
- [ ] External dependencies mocked
- [ ] Tests saved as files before running
- [ ] Test output dirs git‑ignored
- [ ] No commented‑out tests

## 20. Packaging (Standalone Library)
- [ ] Uses pyproject.toml + setuptools
- [ ] Source dir matches project name
- [ ] No ROS2 imports outside `ros/`
- [ ] Examples ≤ 40 lines

## 21. ROS2 Package
- [ ] Nodes under `ros/`
- [ ] Lifecycle nodes where appropriate
- [ ] Converters in `ros/converters.py`
- [ ] Launch files use `better_launch`
- [ ] Runtime deps in `package.xml`

## 22. Dead Code
- [ ] No unreachable code
- [ ] No commented‑out blocks

## 23. Code Quality
- [ ] No duplicated logic. 
- [ ] Look closely for code that can be extracted into a helper
- [ ] No YAGNI features
- [ ] Prefer async/await
- [ ] Avoid complex nested comprehensions
- [ ] Extract helpers when 3+ lines repeat
- 