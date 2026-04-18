import streamlit as st
import base64, random, time, io
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from streamlit_tags import st_tags
from PIL import Image
import nltk

nltk.download('stopwords')

# ROLE based SKILLS needed
role_skills = {
    "data scientist": ["python", "machine learning", "sql", "statistics"],
    "web developer": ["html", "css", "javascript", "react"],
    "android developer": ["java", "kotlin", "android"],
    "manager": ["communication", "leadership", "team management", "project management", "planning"],
    "ui/ux designer": ["figma", "wireframing", "prototyping", "user research"]
}


# ---------- FUNCTIONS ----------
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


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="800"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


# ---------- UI ----------
st.set_page_config(page_title="Resume Analyzer")

st.title("📄 Resume Analyzer")

# 🔹 Role input
role = st.text_input("Enter target role (e.g. Manager, Data Scientist)")

pdf_file = st.file_uploader("Upload Resume", type=["pdf"])

if pdf_file:
    save_path = './Uploaded_Resumes/' + pdf_file.name
    with open(save_path, "wb") as f:
        f.write(pdf_file.getbuffer())

    show_pdf(save_path)

    data = ResumeParser(save_path).get_extracted_data()

    if data:
        st.success("Hello " + str(data.get('name', 'User')))

        skills = data.get('skills', [])
        user_skills = [s.lower() for s in skills]

        st.subheader("🧠 Your Skills")
        st_tags(label='', value=skills)

        # ROLE ANALYSIS
        if role:
            role_lower = role.lower()

            if role_lower in role_skills:
                required = role_skills[role_lower]
                missing = [s for s in required if s not in user_skills]

                st.subheader("📊 Role Analysis")

                st.write("Required Skills:", required)
                st.write("Your Skills:", user_skills)

                if missing:
                    st.error(" Missing Skills:")
                    st.write(missing)
                else:
                    st.success("WOW !!!!! You are well prepared for this role!")

                # MATCH SCORE
                match_score = int((len(required) - len(missing)) / len(required) * 100)

                st.subheader("📈Match Score")
                st.progress(match_score)
                st.success(f"{match_score}% match with {role.title()} role")

            else:
                st.warning("Role not found in system")

    else:
        st.error("Could not parse resume")