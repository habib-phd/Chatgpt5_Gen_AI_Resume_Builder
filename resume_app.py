import os
import gradio as gr
import tempfile
from dotenv import load_dotenv
from openai import OpenAI

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER

# DOCX
from docx import Document

# --------------------
# ENV + CLIENT
# --------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("✅ OpenAI API key loaded")

# --------------------
# PDF GENERATOR (UNICODE SAFE)
# --------------------
def create_pdf(text):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(file.name, pagesize=LETTER)
    content = []

    for line in text.split("\n"):
        if line.strip():
            content.append(Paragraph(line.replace("&", "&amp;"), styles["Normal"]))
            content.append(Spacer(1, 8))

    doc.build(content)
    return file.name

# --------------------
# DOCX GENERATOR
# --------------------
def create_docx(text):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(file.name)
    return file.name

# --------------------
# GPT GENERATION
# --------------------
def generate_documents(
    name,
    location,
    email,
    template,
    experience,
    skills,
    projects,
    need_cover_letter
):
    prompt = f"""
Create a {template} professional resume in clean Markdown.
Make it ATS-optimized, concise, and impactful.

Name: {name}
Location: {location}
Email: {email}

Experience:
{experience}

Skills:
{skills}

Projects:
{projects}
"""

    resume = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {"role": "system", "content": "You are an expert technical resume writer."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=900
    ).choices[0].message.content.strip()

    cover_letter = ""
    if need_cover_letter:
        cover_letter = client.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {"role": "system", "content": "You write professional cover letters."},
                {"role": "user", "content": f"Write a tailored cover letter for this resume:\n{resume}"}
            ],
            max_completion_tokens=500
        ).choices[0].message.content.strip()

    pdf = create_pdf(resume)
    docx = create_docx(resume)

    return resume, cover_letter, pdf, docx

# --------------------
# GRADIO UI
# --------------------
demo = gr.Interface(
    fn=generate_documents,
    inputs=[
        gr.Textbox(label="Full Name", value="Habib Rahimi"),
        gr.Textbox(label="Location", value="Boise, ID"),
        gr.Textbox(label="Email", value="habib@email.com"),
        gr.Dropdown(
            ["Modern Tech", "Classic Professional", "Minimal ATS"],
            label="Resume Template",
            value="Modern Tech"
        ),
        gr.Textbox(
            label="Experience",
            lines=6,
            value="- Web Developer — Python & WordPress\n- Integrated AI APIs\n- Freelance for small businesses"
        ),
        gr.Textbox(
            label="Skills",
            value="Python, WordPress, OpenAI API, Gradio, Streamlit, GitHub"
        ),
        gr.Textbox(
            label="Projects (with links if possible)",
            lines=4,
            value="- AI Resume Generator\n- WordPress Business Site\n- Streamlit AI App"
        ),
        gr.Checkbox(label="Generate Cover Letter", value=True)
    ],
    outputs=[
        gr.Textbox(label="Resume Preview", lines=25),
        gr.Textbox(label="Cover Letter", lines=15),
        gr.File(label="Download PDF"),
        gr.File(label="Download DOCX")
    ],
    title="🚀 AI Resume & Cover Letter Generator",
    description="Portfolio-grade resume builder with PDF + Word export. ATS-safe. Unicode-safe."
)

demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
