# Generate & Export Q/A from PDFs
Screen Recording Demo (Walkthrough): https://screenrec.com/share/35VgUEPlLf <br>

![Screenshot (2453)](https://github.com/AnUbHaVafs/Generate_and_Export_QAs_from_PDFS/assets/76126067/8d93a74e-c4f0-4994-9278-3218113be95c)

add them as reviweer
<h3>Generate Questions and Answers and Export them as PDF</h3>
<h3>How to Setup ?</h3> 
Create a virtual environment:
<ul>
  <ol>
    <li>conda create -p venv python==3.10</li>
    <li>conda activate venv/</li>
    <li>Get you GOOGLE_API_KEY from "https://makersuite.google.com/app/apikey"</li>
    <li>Create a .env file and place this key value pair</li>
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    Note: Replace YOUR_GOOGLE_API_KEY with your own API key from makersuite.google.com
    <li>pip install -r requirements.txt</li>
    <li>Also install these 2 via terminal:</li>
    pip install reportlab<br>  
    pip install fpdf<br>
    <li>streamlit run chatWithPDF.py</li>
  </ol>
</ul>
<h2>Features</h2>
<h4>Uploads Multiple varied PDFs</h4>
<h4>Generate Questions of different types: MCQS, T/F, Objective, Subjective</h4>
<h4>Export Quesitons and Answers generated as PDF</h4>
<h4>Queries your PDFs</h4>
  
<h2>A summary report</h2> <br>
<h3>Approach Taken</h3>
1. Went First through Official Docs of LangChain(really helpful), Gemini Pro, Google Embeddings.
2. Read from other sources: medium blogs, articles.
3. Created the Environment needed, started implementing the basic requirements according to the docs until matches our requirements.
<h3>Challenges Faced</h3>
1. Never created any similar LLM-based project before, so did go through basics first to understand the fundamentals under given time.
2. Going through 3 new full documentations was challenging task.<br>
<h2>Suggestions for Improvement</h2>
1. retrieval_chain could be given access to fetch data from multiple online sources if not found accurate details in pdfs uploaded by users.<br>
2. More paramters could be added like Create Tests and assign marks to each questions according to their difficulties and send it to shared email ids. <br>
Thank You <br>
Anubhav Agrawal <br>
