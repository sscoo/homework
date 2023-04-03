import streamlit as st
import os
from captcha.image import ImageCaptcha
import random
from PIL import Image

# Set the title and favicon of the web page
st.set_page_config(page_title="File Submission Form", page_icon=":file_folder:")

# Set the upload directory for storing uploaded files
UPLOAD_DIR = "./uploads"

# Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Define the form fields
st.write("# File Submission Form")
name = st.text_input("Name")
student_id = st.text_input("Student ID")
file = st.file_uploader("Upload a file")
captcha = st.empty()
# Generate a random captcha image
if 'captcha_text' not in st.session_state:
    image = ImageCaptcha()
    captcha_text = str(random.randint(1000, 9999))
    captcha_image = Image.open(image.generate(captcha_text))
    st.session_state.captcha_text = captcha_text
    st.session_state.captcha_image = captcha_image

else:
    captcha_image = st.session_state.captcha_image
    captcha_text = st.session_state.captcha_text

# Display the captcha image
captcha = st.image(captcha_image)

# Check if the form is complete and valid
if name and student_id and file and st.text_input("Enter the captcha code") == captcha_text:
    # Save the uploaded file to the upload directory
    filename = os.path.join(UPLOAD_DIR, file.name)
    with open(filename, "wb") as f:
        f.write(file.getbuffer())

    # Display a success message
    st.write("File uploaded successfully!")
else:
    # Display a warning message if the form is incomplete or the captcha code is incorrect
    if name or student_id or file:
        st.warning("Please enter the correct captcha code.")
    else:
        st.warning("Please fill in all the form fields and upload a file.")