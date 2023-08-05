from PyPDF2 import PdfReader
import pinecone
import openai
import requests

model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = "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"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}



openai.api_key = "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"

pinecone_api = "63d6a129-c87b-4108-a29b-15ccc989958c"
pinecone_env = "northamerica-northeast1-gcp"
pinecone.init(api_key=pinecone_api, environment=pinecone_env)
index = pinecone.Index("newp")


def text_embedding(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
    return response.json()


def upsert_pinecorn(id, emb, con):
    index.upsert([(id, emb, con)])
    return "seccess"

def pdf_read(file):
    reader = PdfReader(file)
    # for i in range(len(reader.pages)):
    page = reader.pages[0]
        # print(len(page.extract_text().split('\n')))
    upsert(page.extract_text().split('\n'))
    # print(cnt)

def upsert(contents):
    index_num = 500
    
    for content in contents:
        index_num+=1
        embeded_content = text_embedding(content)
        upsert_id = "vec" + str(index_num)
        upsert_response = upsert_pinecorn(upsert_id, embeded_content, {"content": content})
    print(upsert_response)

messages = [ {"roll": "system", "content" : "You are a intelligent assistant."}]

def semantic_search(embeded_query):
    result = index.query(
        top_k=10,
        vector=embeded_query,
        include_metadata=True,
        include_values=True
    )
    res_content = []
    for match in result['matches']:
        res_content.append(match['metadata']['content'])
    message = "make short and readable for the follow content.  "
  
    for text in res_content:
        message+= text
  
    messages.append(
        {"roll": "user", "content": messages}
    )

    chat = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", messages = messages
    )

    # reply = chat.choices[0].message.content
    # messages.append(
    #     {"roll":"assistant", "content":reply}
    # )

    # return reply

