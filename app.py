import os
import streamlit as st
from sqlalchemy import create_engine, text

# --- Constants & Countries ---
COUNTRIES = [
    "Russia", "Germany", "Italy", "New Zealand",
    "Netherlands", "Saudi Arabia", "Japan", "Serbia"
]

# --- Database setup (Railway provides DATABASE_URL) ---
DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    """Create the votes table and seed each country if missing."""
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS votes (
              country TEXT PRIMARY KEY,
              count   INTEGER NOT NULL
            );
        """))
        for c in COUNTRIES:
            conn.execute(text("""
                INSERT INTO votes(country, count)
                VALUES (:country, 0)
                ON CONFLICT (country) DO NOTHING;
            """), {"country": c})

def load_votes():
    """Load current tallies from Postgres into a dict."""
    init_db()
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT country, count FROM votes")).all()
    return {r.country: r.count for r in rows}

def save_votes(votes):
    """Persist the in‑memory vote dict back to Postgres."""
    with engine.begin() as conn:
        for country, cnt in votes.items():
            conn.execute(text("""
                UPDATE votes
                SET count = :count
                WHERE country = :country;
            """), {"count": cnt, "country": country})

# --- Initialize session state from DB ---
if 'votes' not in st.session_state:
    st.session_state.votes = load_votes()
if 'vote_cast' not in st.session_state:
    st.session_state.vote_cast = False
if 'finished' not in st.session_state:
    st.session_state.finished = False

# --- Callbacks ---
def cast_vote(country: str):
    st.session_state.votes[country] += 1
    save_votes(st.session_state.votes)
    st.session_state.vote_cast = True

def next_vote():
    st.session_state.vote_cast = False

def reset_votes():
    st.session_state.votes = {c: 0 for c in COUNTRIES}
    save_votes(st.session_state.votes)
    st.session_state.vote_cast = False
    st.session_state.finished = False

# --- Sidebar (Teacher Panel) ---
st.sidebar.header("Teacher Panel")

if st.sidebar.button("Reset votes"):
    reset_votes()
    st.sidebar.success("✅ Votes have been reset.")

if st.sidebar.button("Finish vote"):
    st.session_state.finished = True

st.sidebar.markdown("---")
st.sidebar.download_button(
    label="📥 Download votes.json",
    data=st.session_state.votes,
    file_name="votes.json",
    mime="application/json"
)

# --- Finished: Show Results & Winner ---
if st.session_state.finished:
    st.header("🏆 Election Results")
    for country, count in st.session_state.votes.items():
        st.write(f"{country}: {count} vote{'s' if count != 1 else ''}")
    max_votes = max(st.session_state.votes.values())
    winners = [c for c, v in st.session_state.votes.items() if v == max_votes]
    if max_votes == 0:
        st.warning("No votes have been cast.")
    elif len(winners) == 1:
        st.success(f"The winning class is **{winners[0]}** with {max_votes} votes!")
    else:
        st.success(f"It's a tie between: {', '.join(winners)} ({max_votes} votes each)!")
    st.stop()

# --- Voting Screen ---
st.title("🌐 International Day: Vote for the Best Class")

if not st.session_state.vote_cast:
    codes = {
        "Russia": "ru", "Germany": "de", "Italy": "it", "New Zealand": "nz",
        "Netherlands": "nl", "Saudi Arabia": "sa", "Japan": "jp", "Serbia": "rs"
    }
    for row in range(2):
        cols = st.columns(4)
        for idx, country in enumerate(COUNTRIES[row*4:(row+1)*4]):
            with cols[idx]:
                flag_url = f"https://flagcdn.com/w160/{codes[country]}.png"
                st.image(flag_url, use_container_width=True)
                st.button(
                    country,
                    key=country,
                    on_click=cast_vote,
                    args=(country,)
                )
else:
    st.markdown("### 🥳 Thank you for your vote!")
    st.button("Next vote", on_click=next_vote)

# --- Footer & Branding ---
st.markdown("<hr style='border: 1px solid #A02040;'>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: left;'>
        <p>© Created by Nadia Urban for Shanghai Thomas School</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.image("school_logo.png", width=150)
