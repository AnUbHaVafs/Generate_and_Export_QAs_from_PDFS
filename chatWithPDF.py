import streamlit as st
import base64
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from fpdf import FPDF


load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize session state 
# store the questions generated for entire session
if 'ques_ans_generated' not in st.session_state:
    st.session_state.ques_ans_generated = ""


def extract_text_from_pdfs(pdf_filepaths):
    combined_text =""

    for pdf in pdf_filepaths:
        entire_pdf= PdfReader(pdf)
        for page in entire_pdf.pages:
            combined_text += page.extract_text()

    return combined_text


def get_text_chunks(text):
    chunk_size = 10000
    chunk_overlap = 1000

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    text_chunks = text_splitter.split_text(text)

    return text_chunks


def get_vector_store(text_chunks):
    embedding_model_path = "models/embedding-001"
    embeddings = GoogleGenerativeAIEmbeddings(model = embedding_model_path)

    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """
    Please answer the following question based on the information provided in the context in most detailed manner as possible, ensure to provide all the details, if the answer is not in
    provided context just utter, "answer is not avaliable", never provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


def user_input(user_question, topics, chapters, subjects, class_levels, question_type, ques_ans_generated):

    create_questions = 'create questions with detailed answers only from these'
    append_topics = '' if len(topics) == 0 else f' topics: {topics} and '
    append_chapters = '' if len(chapters) == 0 else f' chapters: {chapters} and '
    append_subjects = '' if len(subjects) == 0 else f' subjects: {subjects} and '
    append_classes = '' if len(class_levels) == 0 else f' class standards: {class_levels} and '
    append_question_type = '' if len(class_levels) == 0 else f' all questions must be of type: {question_type} with their answers as well'

    modified_user_question = create_questions + append_topics + append_chapters + append_subjects + append_classes + append_question_type
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(modified_user_question)

    chain = get_conversational_chain()    
    response = chain(
        {"input_documents":docs, "question": modified_user_question}, return_only_outputs=True)
    # storing the response in session # tab 1
    st.session_state.ques_ans_generated = response["output_text"]


# to answer user queries about pdfs
def hanlde_user_query(user_question):
    
    create_questions = 'create questions and answers from these pdfs'
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(create_questions)

    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "question": create_questions}, return_only_outputs=True)
    # tab 2
    st.write(response["output_text"])


def export_questions_as_pdf(text):
    pdf_filename = "exported_text.pdf"

    # Create a PDF document
    c = canvas.Canvas(pdf_filename)

    # Add text to the PDF
    c.drawString(100, 750, text)

    # Save the PDF
    c.save()

    return pdf_filename


def create_download_link(val, filename):
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'


def main():
    st.set_page_config("Generate Q/A", layout="wide")
    st.header("Generate & Export Q/A from PDFs")
    
    # background css from wave.css at componentWillLoad
    with open('./wave.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # tabs for different use-cases
    tab1, tab2, tab3, tab4 = st.tabs(["Filters on Questions  ", "Questions Generated  ", "Export PDF ", "Ask Questions from PDF"])

    # filters on questions
    with tab1:

        # Additional input elements for specifying topics, chapters, subjects, and class levels
        topics = st.text_input("Enter Topics (comma-separated)")        
        chapters = st.text_input("Enter Chapters (comma-separated)")
        subjects = st.text_input("Enter Subjects (comma-separated)")
        class_levels = st.text_input("Enter Class Levels (comma-separated)")
        question_type = st.radio('Questions Type:', [" Multiple Choice ", "True/False", "Fill-in-the-blank", "Subjective (essay-style)"])

        user_question = st.button('Generate Questions')
        if user_question:
            user_input(user_question, topics, chapters, subjects, class_levels, question_type, st.session_state.ques_ans_generated)


    # questions generated
    with tab2 :
        st.write(st.session_state.ques_ans_generated)


    # export pdf
    with tab3:
        export_questions = st.button("Export as PDF")


    # ask questions from pdf     
    with tab4:
        st.header("Ask Questions From PDFs")
        user_query_question = st.text_input("Ask a Question from the PDF Files")    
        if user_query_question:
           hanlde_user_query(user_query_question)       
         
            
    # export questions_generated PDF         
    if export_questions:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.multi_cell(0, 10, st.session_state.ques_ans_generated.encode("utf-8").decode("latin-1"))
        html = create_download_link(pdf.output(dest="S").encode("latin-1"), "Q/A_exported")
        st.markdown(html, unsafe_allow_html=True)

    # pdf uploader sidebar
    with st.sidebar:
        st.title("PDFs:")        
        pdf_docs = st.file_uploader("Upload PDF Files and Click on Submit & Process", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = extract_text_from_pdfs(pdf_docs)                
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")

if __name__ == "__main__":
    main()


