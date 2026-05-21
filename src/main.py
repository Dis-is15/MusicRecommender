import streamlit as st
from recommend import df, recommend_songs

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TUNIFY — Music Recommender",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --black:   #0a0a0a;
    --surface: #111111;
    --card:    #191919;
    --border:  #2a2a2a;
    --lime:    #c6f135;
    --lime-dim:#8fad24;
    --white:   #f0ede6;
    --muted:   #6b6b6b;
    --radius:  14px;
}

/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--black) !important;
}
[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
[data-testid="stHeader"] { display: none; }
footer { display: none !important; }
.block-container { max-width: 680px; padding: 3rem 1.5rem 4rem; }

* { font-family: 'DM Sans', sans-serif; color: var(--white); }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-tag {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--lime);
    background: rgba(198,241,53,0.10);
    border: 1px solid rgba(198,241,53,0.25);
    padding: 5px 14px;
    border-radius: 99px;
    margin-bottom: 1.4rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.8rem, 12vw, 7rem);
    letter-spacing: 0.03em;
    line-height: 0.92;
    color: var(--white);
    margin: 0 0 1.2rem;
}
.hero-title span { color: var(--lime); }
.hero-sub {
    font-size: 0.97rem;
    color: var(--muted);
    font-weight: 300;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
    text-align: center;
}

/* ── Vinyl decoration ── */
.vinyl-wrap {
    display: flex;
    justify-content: center;
    margin: 0.5rem 0 2.5rem;
}
.vinyl {
    width: 84px; height: 84px;
    border-radius: 50%;
    background: conic-gradient(
        #1a1a1a 0deg 30deg, #222 30deg 60deg,
        #1a1a1a 60deg 90deg, #222 90deg 120deg,
        #1a1a1a 120deg 150deg, #222 150deg 180deg,
        #1a1a1a 180deg 210deg, #222 210deg 240deg,
        #1a1a1a 240deg 270deg, #222 270deg 300deg,
        #1a1a1a 300deg 330deg, #222 330deg 360deg
    );
    box-shadow: 0 0 0 3px #2c2c2c, 0 0 28px rgba(198,241,53,0.18);
    animation: spin 6s linear infinite;
    position: relative;
    display: flex; align-items: center; justify-content: center;
}
.vinyl::after {
    content: '';
    width: 22px; height: 22px;
    border-radius: 50%;
    background: var(--lime);
    box-shadow: 0 0 12px rgba(198,241,53,0.6);
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Select box label ── */
.select-label {
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}

/* ── Streamlit selectbox overrides ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--white) !important;
    font-size: 1rem !important;
    padding: 0.6rem 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--lime) !important;
    box-shadow: 0 0 0 3px rgba(198,241,53,0.12) !important;
}
/* Selected value text — broad net to beat Streamlit specificity */
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] p,
[data-testid="stSelectbox"] div[class*="singleValue"],
[data-testid="stSelectbox"] div[class*="ValueContainer"] *,
[data-testid="stSelectbox"] div[class*="placeholder"],
[data-testid="stSelectbox"] input,
[data-testid="stSelectbox"] [data-baseweb="select"] *,
[data-testid="stSelectbox"] [role="combobox"] * {
    color: var(--white) !important;
    -webkit-text-fill-color: var(--white) !important;
}
/* Dropdown menu panel */
[data-testid="stSelectbox"] ul,
[data-testid="stSelectbox"] [class*="menu"],
[data-testid="stSelectbox"] [class*="MenuList"],
div[class*="stSelectbox"] [class*="option"] {
    background: var(--card) !important;
    color: var(--white) !important;
}
/* Each option row */
[class*="option"] {
    background: var(--card) !important;
    color: var(--white) !important;
}
[class*="option"]:hover,
[class*="option--is-focused"] {
    background: var(--border) !important;
    color: var(--lime) !important;
}
[class*="option--is-selected"] {
    background: rgba(198,241,53,0.12) !important;
    color: var(--lime) !important;
}
/* Dropdown arrow icon */
[data-testid="stSelectbox"] svg { fill: var(--muted) !important; }

/* ── Primary button ── */
[data-testid="stButton"] > button,
[data-testid="stButton"] > button p,
[data-testid="stButton"] > button span {
    color: #0a0a0a !important;
    -webkit-text-fill-color: #0a0a0a !important;
}
[data-testid="stButton"] > button {
    width: 100%;
    background: var(--lime) !important;
    color: #0a0a0a !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.25rem !important;
    letter-spacing: 0.1em !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.85rem 2rem !important;
    margin-top: 1.2rem;
    cursor: pointer;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 4px 24px rgba(198,241,53,0.25) !important;
}
[data-testid="stButton"] > button:hover {
    background: #d8ff40 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(198,241,53,0.35) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--lime) !important; }

/* ── Results section ── */
.results-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 2.5rem 0 1.2rem;
}
.results-line {
    flex: 1;
    height: 1px;
    background: var(--border);
}
.results-title {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    white-space: nowrap;
}

/* ── Song cards ── */
.song-card {
    display: flex;
    align-items: center;
    gap: 16px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.25rem;
    margin-bottom: 10px;
    transition: border-color 0.2s, transform 0.2s;
    animation: slideUp 0.4s ease both;
}
.song-card:hover {
    border-color: var(--lime);
    transform: translateX(4px);
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.card-rank {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    color: var(--lime);
    min-width: 28px;
    line-height: 1;
}
.card-info { flex: 1; min-width: 0; }
.card-song {
    font-size: 0.97rem;
    font-weight: 500;
    color: var(--white);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.card-artist {
    font-size: 0.8rem;
    color: var(--muted);
    margin-top: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.card-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--border);
    flex-shrink: 0;
    transition: background 0.2s;
}
.song-card:hover .card-dot { background: var(--lime); }

/* ── Warning / info ── */
[data-testid="stWarning"] {
    background: rgba(255,180,0,0.08) !important;
    border: 1px solid rgba(255,180,0,0.2) !important;
    border-radius: var(--radius) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--black); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1 class="hero-title">TUN<span>i</span>FY</h1>
    <p class="hero-sub">Drop a track you love. We'll find the ones you didn't know you needed.</p>
</div>
<div class="vinyl-wrap">
    <div class="vinyl"></div>
</div>
""", unsafe_allow_html=True)


# ── Song selector ─────────────────────────────────────────────────────────────
st.markdown('<p class="select-label">Choose a song</p>', unsafe_allow_html=True)
song_list = sorted(df['song'].dropna().unique())
selected_song = st.selectbox("", song_list, label_visibility="collapsed")

recommend_clicked = st.button("FIND SIMILAR TRACKS →")


# ── Recommendations ───────────────────────────────────────────────────────────
if recommend_clicked:
    with st.spinner("Tuning in..."):
        recommendations = recommend_songs(selected_song)

    if recommendations is None or recommendations.empty:
        st.warning("Hmm, we couldn't find that track in our library.")
    else:
        st.markdown("""
        <div class="results-header">
            <div class="results-line"></div>
            <span class="results-title">Top Picks For You</span>
            <div class="results-line"></div>
        </div>
        """, unsafe_allow_html=True)

        # Detect column names flexibly
        song_col   = next((c for c in recommendations.columns if 'song'   in c.lower()), recommendations.columns[0])
        artist_col = next((c for c in recommendations.columns if 'artist' in c.lower()), None)

        for i, row in recommendations.iterrows():
            rank   = int(i) + 1 if isinstance(i, int) else recommendations.index.get_loc(i) + 1
            song   = row[song_col]
            artist = row[artist_col] if artist_col else "Unknown Artist"

            st.markdown(f"""
            <div class="song-card" style="animation-delay:{(rank-1)*0.07}s">
                <span class="card-rank">{rank:02d}</span>
                <div class="card-info">
                    <div class="card-song">{song}</div>
                    <div class="card-artist">{artist}</div>
                </div>
                <div class="card-dot"></div>
            </div>
            """, unsafe_allow_html=True)