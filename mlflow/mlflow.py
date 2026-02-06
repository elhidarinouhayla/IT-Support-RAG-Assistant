# import mlflow
# import time
# from utils.embedding import save_vectordb, configuration

# mlflow.set_tracking_uri("file:./mlruns")
# mlflow.set_experiment("RAG_IT_SUPPORT")

# question = "Quelles sont les informations importantes mentionnees dans le document ?"

# with mlflow.start_run(run_name="RAG_Gemini_Run"):

#     start_time = time.time()

#     mlflow.log_param("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")
#     mlflow.log_param("llm_model", "gemini-flash-latest")
#     mlflow.log_param("vector_db_path", "../data/vectordb/chroma_db")

#     vector_db = save_vectordb()
#     rag_chain = configuration(vector_db)

#     answer = rag_chain.invoke({"query": question})

#     latency = (time.time() - start_time) * 1000
#     mlflow.log_metric("latency_ms", latency)

#     mlflow.log_text(answer["result"], "test_answer.txt")

#     print("Réponse MLflow :")
#     print(answer["result"])
#     # print(f"Latence : {latency:.2f} ms")
