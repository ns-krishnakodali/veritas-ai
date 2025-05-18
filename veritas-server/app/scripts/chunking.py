from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(text_data: str, chunk_size: int = 500, chunk_overlap: int = 100) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return text_splitter.split_text(text_data)


def chunk_json(json_data: str, chunk_size: int = 500, chunk_overlap: int = 100) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    all_chunks = []
    for data in json_data:
        chunks = text_splitter.split_text(data)
        all_chunks.extend(chunks)

    return all_chunks
