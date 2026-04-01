from langchain_community.document_loaders import PyPDFLoader

def pdf_load(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    for doc in docs:
        text = doc.page_content
        text = text.replace("\n", " ")
        text = " ".join(text.split())
        doc.page_content = text

    return docs
