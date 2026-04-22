# **Resume Analyser With NLP on Streamlit**

   
## Installation

To install the libraries used in this project. Follow the 
below steps:

```bash

#SET UP:

# 1. INSTALL BELOW LIBRARIES

        #pip install -r requirements.txt

        # pip install nltk

        # pip install spacy==2.3.5

        # pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz

        # pip install pyresparser

# 2. CREAT A FOLDER AND NAME IT (e.g. resume)

        #2.1 create two more folders inside this folder (Logo and Uploaded_Resumes)
        #2.2 create two python files (App.py and Courses.py)



# 3. CONTINUE WITH THE FOLLOWING CODE...

import streamlit as st
import pandas as pd
import base64,random
import time,datetime
#libraries to parse the resume pdf files
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course,web_course,android_course,ios_course,uiux_course
import plotly.express as px #to create visualisations at the admin session
import nltk
nltk.download('stopwords')

```
    

To run tests, run the following command

```bash
  streamlit run App.py
```

## 🚀 About Me

Data Scientist Enthusiast | Engineer Graduate | Solving Problems Using Data 


# Hi, I'm Shreya B! 👋



## Tech Stack









## 🛠 Skills
1. Data Scientist
2. Data Analyst
3. Machine Learning 


## Future Plans 

⚡️ Looking forward to help drive innovations into your company as a Data Scientist

⚡️ Looking forward to offer more than I take and leave the place better than i found
