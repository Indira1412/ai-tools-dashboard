from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = ["AI is changing the world"]

embedding = model.encode(text)

print("Embedding length:", len(embedding[0]))
print("First numbers:", embedding[0][:10])