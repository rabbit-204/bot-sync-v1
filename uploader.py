from openai import OpenAI
import os

def sync_to_openai(client, vector_store_id, files_to_upload):
    if not files_to_upload:
        return 0

    file_ids = []
    for file_path in files_to_upload:
        with open(file_path, "rb") as f:
            response = client.files.create(file=f, purpose="assistants")
            file_ids.append(response.id)
            print(f"Uploaded {file_path} (ID: {response.id})")

    if file_ids:
        print(f"Adding {len(file_ids)} files to Vector Store: {vector_store_id}")
        
        vector_stores = getattr(client.beta, "vector_stores", None)
        if vector_stores is None:
            raise AttributeError("Thư viện OpenAI của bạn quá cũ. Hãy chạy: pip install --upgrade openai")
            
        batch = vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store_id,
            file_ids=file_ids
        )
        print(f"Batch status: {batch.status}")
        return batch.file_counts.completed
    return 0