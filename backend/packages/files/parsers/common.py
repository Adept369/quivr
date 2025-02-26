import time

import tiktoken
from logger import get_logger
from models import File
from modules.brain.service.brain_vector_service import BrainVectorService
from packages.embeddings.vectors import Neurons
from repository.files.upload_file import DocumentSerializable

logger = get_logger(__name__)


async def process_file(
    file: File,
    loader_class,
    brain_id,
    original_file_name,
    integration=None,
    integration_link=None,
):
    dateshort = time.strftime("%Y%m%d")
    neurons = Neurons()

    file.compute_documents(loader_class)

    metadata = {
        "file_sha1": file.file_sha1,
        "file_size": file.file_size,
        "file_name": file.file_name,
        "chunk_size": file.chunk_size,
        "chunk_overlap": file.chunk_overlap,
        "date": dateshort,
        "original_file_name": original_file_name or file.file_name,
        "integration": integration or "",
        "integration_link": integration_link or "",
    }
    docs = []

    enc = tiktoken.get_encoding("cl100k_base")

    if file.documents is not None:
        for doc in file.documents:  # pyright: ignore reportPrivateUsage=none
            new_metadata = metadata.copy()
            len_chunk = len(enc.encode(doc.page_content))
            logger.info(f"Chunk size: {len_chunk}")
            new_metadata["chunk_size"] = len_chunk
            doc_with_metadata = DocumentSerializable(
                page_content=doc.page_content, metadata=new_metadata
            )
            docs.append(doc_with_metadata)

    created_vector = neurons.create_vector(docs)

    brain_vector_service = BrainVectorService(brain_id)
    for created_vector_id in created_vector:
        result = brain_vector_service.create_brain_vector(
            created_vector_id, metadata["file_sha1"]
        )
        logger.debug(f"Brain vector created: {result}")

    if created_vector:
        return len(created_vector)
    else:
        return 0
