# Contributing to the B2B Fleet Aggregator API

First off, thank you for considering contributing to this project! We value collaborative engineering and strict code quality.

## 🛠️ Local Development Setup

1. **Clone the repository:** `git clone https://github.com/sandesh-s-hegde/b2b-fleet-aggregator-api`
2. **Create a virtual environment:** `python -m venv venv && source venv/bin/activate`
3. **Install dependencies:** `pip install -r requirements.txt`
4. **Run the server:** `uvicorn main:app --reload`

## 📝 Commit Message Standards

This project strictly adheres to [Conventional Commits](https://www.conventionalcommits.org/). This allows us to auto-generate changelogs and maintain a clean Git history.

Your commit messages must be formatted as follows:
` <type>(<scope>): <short summary>`

**Allowed Types:**
* `feat`: A new feature (e.g., a new API endpoint)
* `fix`: A bug fix
* `docs`: Documentation changes
* `chore`: Maintenance, CI/CD, or dependency updates
* `refactor`: Code changes that neither fix a bug nor add a feature

## 🚀 Pull Request Process

1. Create a feature branch from `main` (e.g., `feature/surge-pricing`).
2. Ensure your code passes all local linting (`flake8`) and formatting (`black`).
3. Submit a Pull Request using the provided PR template.
4. Request a review from the core maintainers.
