import streamlit as st
import base64, io
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from streamlit_tags import st_tags
import nltk
import spacy

# Setup
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")

# ---------- PDF TO TEXT ----------
def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            interpreter.process_page(page)

    text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text


# ---------- EXTRACT SKILLS FROM STRUCTURED SECTION ----------
def extract_skills_from_resume_text(text):
    skills = set()

    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if ":" in line:
            left, right = line.split(":", 1)

            # skip very long sentences (avoid experience section)
            if len(right.split(",")) >= 2:   # ensures it's a list of skills
                for skill in right.split(","):
                    clean = skill.strip().lower()
                    if len(clean) > 2:
                        skills.add(clean)

    return list(skills)


# ---------- CLEANING ----------
def clean_resume_skills(skills):
    remove_words = {
        "word", "pdf", "system", "video", "health",
        "technical", "analysis", "analyze", "training", "engineering"
    }

    cleaned = []
    for skill in skills:
        s = skill.lower().strip()
        if s not in remove_words and len(s) > 2:
            cleaned.append(s)

    return list(set(cleaned))


# ---------- JD EXTRACTION ----------
def extract_skills_from_jd(jd_text):
    doc = nlp(jd_text)

    skills = set()

    for chunk in doc.noun_chunks:
        text = chunk.text.lower().strip()

        if len(text) > 2 and not text.isdigit():
            skills.add(text)

    return list(skills)


# ---------- PDF VIEW ----------
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


# ---------- UI ----------
st.set_page_config(page_title="Resume Analyzer")
st.title("📄 AI Resume Analyzer")

job_desc = st.text_area("📄 Paste Job Description")
pdf_file = st.file_uploader("Upload Resume", type=["pdf"])


# ---------- MAIN ----------
if pdf_file:
    save_path = './Uploaded_Resumes/' + pdf_file.name

    with open(save_path, "wb") as f:
        f.write(pdf_file.getbuffer())

    show_pdf(save_path)

    # Extract full text
    resume_text = pdf_reader(save_path)

    # Extract structured skills (YOUR SECTION)
    manual_skills = extract_skills_from_resume_text(resume_text)

    # Extract using pyresparser
    data = ResumeParser(save_path).get_extracted_data()

    if data:
        st.success("Hello " + str(data.get('name', 'User')))

        raw_skills = data.get('skills', [])

        # COMBINE BOTH
        combined_skills = raw_skills + manual_skills

        # CLEAN FINAL SKILLS
        user_skills = clean_resume_skills(combined_skills)

        st.subheader(" Your Skills")
        st_tags(label='', value=user_skills)

        # ---------- JD ANALYSIS ----------
        if job_desc:
            jd_skills = extract_skills_from_jd(job_desc)

            st.subheader("📊 Job Description Analysis")
            st.write("Extracted JD Skills:", jd_skills)

            matched = []
            missing = []

            for jd_skill in jd_skills:
                if any(jd_skill in us or us in jd_skill for us in user_skills):
                    matched.append(jd_skill)
                else:
                    missing.append(jd_skill)

            st.write("Your Skills:", user_skills)

            if missing:
                st.error(" Missing Skills:")
                st.write(missing)
            else:
                st.success(" Great match!")

            # MATCH SCORE
            if len(jd_skills) > 0:
                match_score = int(len(matched) / len(jd_skills) * 100)
            else:
                match_score = 0

            st.subheader("📈 Match Score")
            st.progress(match_score)
            st.success(f"{match_score}% match with this job")

    else:
        st.error("Could not parse resume")
