# Tunify — Music Recommendation App

> Drop a track you love. We'll find the ones you didn't know you needed.

Tunify is a content-based music recommender built with Python and Streamlit. It analyzes song lyrics using TF-IDF vectorization and cosine similarity to surface tracks that feel sonically and lyrically similar to whatever you're already listening to.

---

## Demo

<img width="1896" height="961" alt="image" src="https://github.com/user-attachments/assets/a6c0ee11-64ce-411d-a4fa-824ea85ea484" />


## How It Works

1. **Preprocessing** — Song lyrics are cleaned (lowercased, stopwords removed, punctuation stripped) and vectorized into a TF-IDF matrix.
2. **Similarity** — A cosine similarity matrix is computed across all songs and saved to disk.
3. **Recommendation** — When you pick a song, Tunify looks up its row in the similarity matrix and returns the top 5 closest matches.



 Add the dataset

Download the [Spotify Million Song Dataset](https://www.kaggle.com/datasets/notshrirang/spotify-million-song-dataset) from Kaggle and place `spotify_millsongdata.csv` in the project root.

## Configuration

| Parameter | Location | Default | Description |
|---|---|---|---|
| `sample size` | `preprocess.py` | `10000` | Number of songs sampled from the dataset |
| `max_features` | `preprocess.py` | `5000` | Max terms in the TF-IDF vocabulary |
| `top_n` | `recommend.py` | `5` | Number of recommendations returned |

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| NLP | NLTK, scikit-learn (TF-IDF) |
| Similarity | Cosine Similarity |
| Persistence | joblib |
| Styling | Custom CSS (Bebas Neue + DM Sans) |

---

## Limitations

- Recommendations are **lyric-based only** — audio features (tempo, key, energy) are not considered.
- The dataset is **sampled** to 10,000 songs on each preprocessing run, so results may vary between runs.
- Songs not present in the sampled dataset will return no results.

---

## License

MIT
