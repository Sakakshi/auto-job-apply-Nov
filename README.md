# Automated Job Application System

An intelligent AI-powered system that automates job applications by matching your profile with job listings, generating customized resumes and cover letters, and streamlining the application process.

## Features

- 🎯 **Smart Job Matching**: AI-powered matching with percentage scores
- 📄 **Dynamic Document Generation**: Custom resumes and cover letters for each job
- 🤖 **Automation**: Automated form filling and application submission
- 👀 **Human Approval**: Review and approve applications before submission
- 📊 **Tracking**: Monitor all applications in one dashboard

## Tech Stack

- **Backend**: Python, LangGraph, SQLAlchemy
- **AI**: Claude API (Anthropic)
- **Automation**: Playwright
- **UI**: Streamlit
- **Database**: SQLite

## Setup

### Prerequisites
- Python 3.10+
- Anthropic API key

### Installation

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\Activate.ps1` (Windows PowerShell)
4. Install dependencies: `pip install -r requirements.txt`
5. Install Playwright browsers: `playwright install`
6. Create `.env` from `.env.example` and add your API key
7. Run: `streamlit run ui/app.py`

## Project Structure

- `config/` - Configuration and settings
- `src/models/` - Data models (User, Job, Application)
- `src/database/` - Database connection and queries
- `src/scrapers/` - Web scrapers for job sites
- `src/matching/` - Job matching algorithm
- `src/generation/` - Resume and cover letter generation
- `src/automation/` - Application automation
- `src/workflows/` - LangGraph workflows
- `ui/` - Streamlit interface
- `tests/` - Unit and integration tests

## Development Roadmap

- [x] Day 1: Project setup and structure
- [ ] Day 2-3: Database models and profile management
- [ ] Day 4-5: Web scraping implementation
- [ ] Day 6-7: Matching algorithm
- [ ] Day 8-9: Document generation
- [ ] Day 10-11: Automation system
- [ ] Day 12+: Testing and refinement

## Daily Development Log

### Day 1 - November 11, 2025
- ✅ Project structure created
- ✅ Dependencies defined
- ✅ Git repository initialized
- ✅ Configuration system set up
- 📝 Next: Database models and profile system

## License

MIT License