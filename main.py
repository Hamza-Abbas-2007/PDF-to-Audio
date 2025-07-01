from flask import render_template
from flask import Flask
from gtts import gTTS
import pymupdf as fitz
import os
from fileinput import filename
from flask import * 
from flask import send_from_directory 

app = Flask(__name__)
language = 'en'

@app.route('/', methods = ['GET','POST'])
def index():
    upload = False
    if request.method == 'POST':  
        f = request.files['file']
        filename = f.filename
        f.save(f.filename) 
        upload = True
    
    if upload == True:
        doc = fitz.open(filename)
        
        # Extract text and save to file
        with open("output.txt", "w", encoding="utf-8") as f:
            for page in doc:
                f.write(page.get_text() + '\n')

        # Read text from file to use with gTTS
        with open("output.txt", "r", encoding="utf-8") as f:
            mytext = f.read()

        # Convert to speech
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("output.mp3")
        
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('.',filename, as_attachment=True)
