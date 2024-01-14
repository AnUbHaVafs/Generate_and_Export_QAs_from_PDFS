# Generate & Export Q/A from PDFs
Screen Recording Demo (Walkthrough): https://screenrec.com/share/35VgUEPlLf <br>

![Screenshot (2453)](https://github.com/AnUbHaVafs/Generate_and_Export_QAs_from_PDFS/assets/76126067/8d93a74e-c4f0-4994-9278-3218113be95c)

add them as reviweer
<h3>Generate Questions and Answers and Export them as PDF</h3>
<h3>How to Setup ?</h3> 
Create a virtual environment:
1. conda create -p venv python==3.10
2. conda activate venv/
3. Get you GOOGLE_API_KEY from "https://makersuite.google.com/app/apikey"
4. Create a .env file and place this key value pair
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
Note: Replace YOUR_GOOGLE_API_KEY with your own API key from makersuite.google.com
5. pip install -r requirements.txt
6. Also install these 2 via terminal:
pip install reportlab<br>  
pip install fpdf<br>
7. streamlit run chatWithPDF.py

A summary report <br>
Thank You <br>
Anubhav Agrawal <br>
