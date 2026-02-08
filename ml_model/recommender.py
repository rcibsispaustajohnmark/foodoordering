import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "tfidf_vectorizer.pkl"), "rb") as f:
    tfidf = pickle.load(f)

with open(os.path.join(BASE_DIR, "cosine_similarity.pkl"), "rb") as f:
    cosine_sim = pickle.load(f)

with open(os.path.join(BASE_DIR, "food_data.pkl"), "rb") as f:
    food = pickle.load(f)


def recommend_food(food_name, top_n=5):
    idx = food[food["name"] == food_name].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]
    food_indices = [i[0] for i in sim_scores]

    return food.iloc[food_indices]["name"].tolist()
