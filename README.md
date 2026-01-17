# ChatGPT-5 Gen AI Resume Builder

An AI-powered resume builder that generates professional resumes using OpenAI and a simple Gradio web interface.

## 🚀 Features
- Generate resumes from user input
- Clean, modern resume formatting
- Download resume as PDF
- Fast and easy web UI using Gradio

## 🧠 Tech Stack
- Python
- OpenAI API
- Gradio
- FPDF2

## 📦 Installation (Local)

Install dependencies:

```bash
pip install -r requirements.txt
▶️ Run the App
python resume_app.py
🔐 Environment Variables
Create a .env file (DO NOT commit this file):
OPENAI_API_KEY=your_api_key_here
🌐 Deployment
GitHub: Source control and versioning
Hugging Face Spaces: Public demo deployment
For Hugging Face:
Add OPENAI_API_KEY in Settings → Variables and secrets
Do not upload .env to the repository
⚠️ Security
API keys are stored securely using:
Environment variables locally
Hugging Face Secrets in production
Sensitive data is never committed to GitHub.
Built by Habibullah Rahimi