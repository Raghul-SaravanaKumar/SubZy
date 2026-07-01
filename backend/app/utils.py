from datetime import datetime
from bson import ObjectId


# ======================================
# Convert MongoDB ObjectId to String
# ======================================
def serialize_document(document: dict):

    if document is None:
        return None

    document["_id"] = str(document["_id"])

    return document


# ======================================
# Convert List of MongoDB Documents
# ======================================
def serialize_documents(documents: list):

    return [
        serialize_document(document)
        for document in documents
    ]


# ======================================
# Get Current UTC Time
# ======================================
def get_current_time():

    return datetime.utcnow()


# ======================================
# Validate MongoDB ObjectId
# ======================================
def is_valid_object_id(id: str):

    return ObjectId.is_valid(id)