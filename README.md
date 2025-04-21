
# Voting App

A simple **Streamlit** application for a school’s International Day where students vote for the best class (by country). Students cast one vote each by clicking on a flag, and a teacher can reset votes or finish the vote to announce the winner.

---

## 📋 Features

- **Student View**
  - Displays 8 country flags in a 4×2 grid.
  - Click a flag to cast a vote, then see a “Thank you for your vote!” message.
  - “Next vote” button to allow another vote.

- **Teacher Panel (Sidebar)**
  - **Reset votes**: clears all tallies back to zero.
  - **Finish vote**: stops voting, displays the full results, and announces the winner (or tie).

---

voting-app/
├── app.py             # Streamlit voting application
├── requirements.txt   # Python dependencies
├── README.md          # This file
├── school_logo.png    # (optional) logo displayed in sidebar/header
└── .gitignore         # (optional) ignore Python caches, etc.

