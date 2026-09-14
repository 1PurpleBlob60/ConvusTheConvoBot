import json
from pathlib import Path

import streamlit as st


FEEDBACK_FILE = Path(__file__).with_name("feedback.json")


def record_feedback(message_index, rating):
	"""Store a thumbs rating in session state and persist it to disk."""
	if "feedback" not in st.session_state:
		st.session_state.feedback = {}

	feedback = "up" if rating == 1 else "down"
	if st.session_state.feedback.get(message_index) == feedback:
		return

	st.session_state.feedback[message_index] = feedback
	FEEDBACK_FILE.write_text(
		json.dumps(st.session_state.feedback, indent=2),
		encoding="utf-8",
	)
