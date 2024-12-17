from .pipe import (
    initialize_database,
    insert_question_answer,
    fetch_last_qa,
    generate_standalone_question_with_llm,
    embed_text,
    setup_faiss,
    retrieve_context,
    call_openai_model,
    load_dataset_and_prepare_faiss,
    classify_intent,
    check_intent_score,
    rag_pipeline_with_db_and_standalone_llm
)

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "A Python package for RAG pipelines using OpenAI and FAISS."
