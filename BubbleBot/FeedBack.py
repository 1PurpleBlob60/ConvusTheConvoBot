import streamlit as st


def record_feedback(message_index, rating):
	"""Store a thumbs rating for an assistant message in the current chat."""
	if "feedback" not in st.session_state:
		st.session_state.feedback = {}

	st.session_state.feedback[message_index] = "up" if rating == 1 else "down"
