import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
from dotenv import load_dotenv

# =============================
# Load Environment
# =============================
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =============================
# Load Gita Dataset (NEW STRUCTURE)
# =============================
# with open("data/gita.json", "r", encoding="utf-8") as f:
#     verses = json.load(f)
from pymongo import MongoClient

mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["krishna_counsel"]
collection = db["gita_verses"]

verses = list(collection.find({}, {"_id": 0}))
print("Total verses loaded:", len(verses))
# =============================
# Prepare Documents for Search
# =============================
documents = []

for v in verses:
    combined_text = f"""
    Teaching: {v.get('teaching', '')}
    Translation: {v.get('translation', '')}
    Commentary: {v.get('commentary', '')}
    Extra Insight: {v.get('extra_insight', '')}
    """
    documents.append(combined_text.strip())

# =============================
# Create TF-IDF Vector Store
# =============================
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(documents)

# =============================
# Retrieval Function
# =============================
def retrieve(query, top_k=3):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

    top_indices = similarities.argsort()[-top_k:][::-1]

    results = []
    for i in top_indices:
        verse_data = verses[i]
        results.append({
            "score": float(similarities[i]),
            "chapter": verse_data["chapter"],
            "verse": verse_data["verse"],
            "teaching": verse_data.get("teaching", ""),
            "translation": verse_data.get("translation", ""),
            "commentary": verse_data.get("commentary", ""),
            "extra_insight": verse_data.get("extra_insight", "")
        })

    return results

# =============================
# Main AI Function
# =============================
def ask_Vrinda(query, history=None):

    retrieved = retrieve(query)

    context_text = "\n\n".join(
        [
            f"""(Relevance: {r['score']:.4f})
Chapter {r['chapter']} Verse {r['verse']}
Teaching: {r['teaching']}
Translation: {r['translation']}
Commentary: {r['commentary']}
Extra Insight: {r['extra_insight']}
"""
            for r in retrieved
        ]
    )

    prompt = f"""
    You are Vrinda — a warm, emotionally intelligent friend.

    IMPORTANT BEHAVIOR RULES:

    1. If the user's message is casual (like "hi", "hey", "what's up"):
       → Respond casually and briefly.
       → Do NOT bring Bhagavad Gita.
       → Do NOT give advice unless asked.

    2. If the user asks for help, guidance, or shares a problem:
       → Respond thoughtfully.
       → Use Bhagavad Gita wisdom only if it truly fits.
       → Keep it simple and practical.

    3. Match the user's energy:
       → Short message = short response.
       → Deep message = deeper response.

    4. Never over-explain.
    5. Never force spiritual knowledge.

    Relevant Gita Context (use only if needed):
    {context_text}

    User Message:
    {query}

Give practical, compassionate, spiritually grounded guidance.
Quote verses naturally if helpful.
"""

    messages = [
        {
            "role": "system",
            "content": "You are Vrinda from Krishna Counsel. Warm, calm, emotionally intelligent."
        }
    ]

    # Add conversation memory (last 6 messages only)
    if history:
        messages.extend(history[-6:])

    # Add current prompt
    messages.append({
        "role": "user",
        "content": prompt
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.5,
        messages=messages
    )

    return response.choices[0].message.content
