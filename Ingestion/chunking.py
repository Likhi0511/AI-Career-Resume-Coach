from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_doc(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80
    )
    return splitter.split_documents(documents)
