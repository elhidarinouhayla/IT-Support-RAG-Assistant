import joblib
import os 
from langchain_community.embeddings import HuggingFaceEmbeddings


kmeans_model = joblib.load("./cluster/models/kmeans_model.pkl")

print('model kmeans charge')


embedding_model = HuggingFaceEmbeddings(
   model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

def cluster(question):
   
   vector = embedding_model.embed_query(question)
   cluster_label = kmeans_model.predict([vector])[0]

   return cluster_label


# question = "Comment contacter le support IT ?"
# predicted_cluster = cluster(question)
# print(f"Question: {question}")
# print(f"Cluster : {predicted_cluster}")