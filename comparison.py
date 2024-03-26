from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncHtmlLoader, DirectoryLoader, TextLoader, PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import requests
import pdfkit

UNSTRUCTURED_URL = "http://localhost:8000/general/v0/general"


def print_with_hashtag(string):
    length = len(string)
    print("#" * (length + 4))
    print("# " + string + " #")
    print("#" * (length + 4))


def print_chunks(chunkers):
    for i, chunk in enumerate(chunkers):
        print_with_hashtag(f"Chunk {i}")
        print(chunk)
        print("\n\n" + "-"*80)

def langchain_print_chunked_pdf(directory):
    print(f"Loading PDF files from: {directory}")
    loader = PyPDFDirectoryLoader(directory)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=10)
    splits = text_splitter.split_documents(docs)
    splits = [split.page_content for split in splits]
    print_chunks(splits)

    # vectorstore.add_documents(documents=splits)

def save_html_as_temp(url):
    requests_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'}
    response = requests.get(url, headers=requests_headers)
    if response.status_code == 200:
        with open("temp.html", "w", encoding="utf-8") as f:
            f.write(response.text)
    else:
        print("Error fetching HTML")
    return "temp.html"

def unstructured_print_chunked_pdf(pdf_path):
    headers = {'accept': 'application/json'}
    MAX_CHARACTERS = 5000
    COMBINE_UNDER_N_CHARS = 2000
    strategy = {"strategy":"hi_res"}
    response = requests.post(UNSTRUCTURED_URL, headers=headers, files={"files": open(pdf_path, "rb")}, data={"strategy": "hi_res" ,"chunking_strategy": "by_title","max_characters": MAX_CHARACTERS, "combine_text_under_n_chars": COMBINE_UNDER_N_CHARS, "overlap": 100})
    if response.status_code == 200:
        # process response.json()
        result = response.json()
        result = [res["text"] for res in result]
        print_chunks(result)
    else:
        print("Error processing request")

def save_url_to_pdf(url):
    pdfkit.from_url(url, "SAVETEST.pdf")

def unstructured_print_chunked_html(url):
    headers = {'accept': 'application/json'}
    MAX_CHARACTERS = 5000
    COMBINE_UNDER_N_CHARS = 1000
    strategy = {"strategy":"hi_res"}
    file = save_html_as_temp(url)
    response = requests.post(UNSTRUCTURED_URL, headers=headers, files={"files": open(file, "rb")}, data={"strategy": "hi_res" ,"chunking_strategy": "by_title","max_characters": MAX_CHARACTERS, "combine_text_under_n_chars": COMBINE_UNDER_N_CHARS, "overlap": 100})
    if response.status_code == 200:
        # process response.json()
        result = response.json()
        result = [res["text"] for res in result]
        print_chunks(result)
    else:
        print("Error processing request")


if __name__ == "__main__":
    # langchain_print_chunked_pdf("./pdf_files")
    # unstructured_print_chunked_pdf("./pdf_files/angr-ext-consecutive.pdf")
    # unstructured_print_chunked_html("https://www.microsoft.com/en-us/security/blog/2018/03/01/finfisher-exposed-a-researchers-tale-of-defeating-traps-tricks-and-complex-virtual-machines/")
    save_url_to_pdf("https://www.microsoft.com/en-us/security/blog/2018/03/01/finfisher-exposed-a-researchers-tale-of-defeating-traps-tricks-and-complex-virtual-machines/")