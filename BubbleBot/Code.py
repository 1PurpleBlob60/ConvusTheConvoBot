import random
import re
from urllib.parse import urlparse

import streamlit as st
import responses as resp
import ifin as ifn


def calculate(first_number, operator, second_number):
    if operator == "+":
        return first_number + second_number
    if operator == "-":
        return first_number - second_number
    if operator == "*":
        return first_number * second_number
    if operator == "/":
        if second_number == 0:
            return "Cannot divide by zero."
        return first_number / second_number


def apply_background(image_address):
    parsed_address = urlparse(image_address)
    if parsed_address.scheme not in {"http", "https"} or not parsed_address.netloc:
        return

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("{image_address}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{
            background: rgba(0, 0, 0, 0);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_button_color(button_color):
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] .stButton > button,
        [data-testid="stChatInput"] button {{
            background-color: {button_color};
            border-color: {button_color};
        }}
        [data-testid="stSidebar"] .stButton > button:hover,
        [data-testid="stSidebar"] .stButton > button:focus,
        [data-testid="stChatInput"] button:hover,
        [data-testid="stChatInput"] button:focus {{
            background-color: {button_color};
            border-color: {button_color};
            color: white;
        }}
        [data-testid="stChatInput"],
        [data-testid="stChatInput"] > div,
        [data-testid="stChatInput"] div[data-baseweb="textarea"] {{
            border-color: {button_color};
        }}
        [data-testid="stChatInput"]:focus-within,
        [data-testid="stChatInput"]:focus-within > div,
        [data-testid="stChatInput"]:focus-within div[data-baseweb="textarea"] {{
            border-color: {button_color};
            box-shadow: 0 0 0 1px {button_color};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def save_button_color():
    selected_color = st.session_state.button_color_picker
    st.session_state.button_color = selected_color
    st.session_state.user_preferences[st.session_state.email] = {
        "button_color": selected_color,
    }


def show_login():
    st.title("Bubble bot🫧")
    st.subheader("Log in to start chatting")

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com")
        username = st.text_input("Username", placeholder="Your name")
        submitted = st.form_submit_button("Log in")

    if submitted:
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email.strip()):
            st.error("Enter a valid email address.")
        elif not username.strip():
            st.error("Enter a username.")
        else:
            normalized_email = email.strip().lower()
            st.session_state.email = normalized_email
            st.session_state.username = username.strip()
            saved_preferences = st.session_state.user_preferences.get(normalized_email, {})
            st.session_state.button_color = saved_preferences.get(
                "button_color",
                st.session_state.button_color,
            )
            st.session_state.button_color_picker = st.session_state.button_color
            st.session_state.logged_in = True
            st.rerun()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "button_color" not in st.session_state:
    st.session_state.button_color = "#ff4b4b"

if "button_color_picker" not in st.session_state:
    st.session_state.button_color_picker = st.session_state.button_color

if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = {}

if not st.session_state.logged_in:
    show_login()
    st.stop()


st.title("Bubble bot🫧")

# 1. Initialize Session State for Chat History & Follow-up tracking
if "messages" not in st.session_state:
    st.session_state.messages = []

if "waiting_for" not in st.session_state:
    st.session_state.waiting_for = None

if "calculator_number" not in st.session_state:
    st.session_state.calculator_number = None

if "calculator_operator" not in st.session_state:
    st.session_state.calculator_operator = None

# Sidebar option to reset/clear chat
with st.sidebar:
    st.header("Settings")
    st.write(f"Logged in as **{st.session_state.username}**")
    if st.button("Change username"):
        st.session_state.changing_username = True

    if st.session_state.get("changing_username", False):
        new_username = st.text_input(
            "New username",
            value=st.session_state.username,
            key="new_username",
        )
        if st.button("Save username"):
            if new_username.strip():
                st.session_state.username = new_username.strip()
                st.session_state.changing_username = False
                st.rerun()
            else:
                st.error("Enter a username.")

    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.pop("email", None)
        st.session_state.pop("username", None)
        st.session_state.pop("changing_username", None)
        st.session_state.pop("new_username", None)
        st.rerun()

    user_icon = st.text_input(
        "User icon",
        value="😶‍🌫",
        help="Enter an emoji."
    )
    assistant_icon = st.text_input(
        "Assistant icon",
        value="🫧",
        help="Enter an emoji."
    )
    background_address = st.text_input(
        "Background image address",
        value="",
        placeholder="https://example.com/image.jpg",
        help="Optional: enter a direct HTTP or HTTPS image address.",
    )
    st.session_state.button_color_picker = st.session_state.button_color
    st.color_picker(
        "Button color",
        key="button_color_picker",
        on_change=save_button_color,
    )
    apply_button_color(st.session_state.button_color)
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.waiting_for = None
        st.session_state.calculator_number = None
        st.session_state.calculator_operator = None
        st.rerun()

if background_address.strip():
    apply_background(background_address.strip())

# 2. Render previous chat messages on rerun
for message in st.session_state.messages:
    if message["role"] == "assistant":
        message_context = st.chat_message("assistant", avatar=assistant_icon)
    else:
        message_context = st.chat_message(
            st.session_state.username,
            avatar=user_icon,
        )

    with message_context:
        st.write(message["content"])

# 3. Handle User Input
if user_input := st.chat_input("Type a message..."):
    # Display user message in chat
    with st.chat_message(st.session_state.username, avatar=user_icon):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    bot_response = ""

    # Check stateful follow-ups first
    if st.session_state.waiting_for == 2:
        bot_response = random.choice(resp.followup2)
        st.session_state.waiting_for = None
    elif st.session_state.waiting_for == 1:
        bot_response = random.choice(resp.followup1)
        st.session_state.waiting_for = None
    elif st.session_state.waiting_for == 3:
        operators = {
            "+": "+",
            "plus": "+",
            "add": "+",
            "-": "-",
            "minus": "-",
            "subtract": "-",
            "*": "*",
            "x": "*",
            "multi": "*",
            "multiply": "*",
            "times": "*",
            "/": "/",
            "divide": "/",
            "divided": "/",
        }
        operator = operators.get(user_input.lower().strip())
        if operator is None:
            bot_response = "Please choose plus, minus, multiply, or divide."
        else:
            st.session_state.calculator_operator = operator
            st.session_state.waiting_for = 4
            bot_response = "What is the second number?"
    elif st.session_state.waiting_for == 4:
        try:
            second_number = float(user_input.strip())
        except ValueError:
            bot_response = "Please enter a number."
        else:
            result = calculate(
                st.session_state.calculator_number,
                st.session_state.calculator_operator,
                second_number,
            )
            bot_response = f"Result: {result:g}" if isinstance(result, float) else result
            st.session_state.waiting_for = None
            st.session_state.calculator_number = None
            st.session_state.calculator_operator = None
    else:
        # Clean string for keyword matching
        cleaned_choice = user_input.lower().strip()
        for sign in ["!", "?", ".", ",", "-"]:
            cleaned_choice = cleaned_choice.replace(sign, "")

        # Logic evaluation
        if cleaned_choice in ifn.special_word:
            bot_response = resp.special_word_resp
        elif cleaned_choice in ifn.question_start2:
            bot_response = random.choice(resp.question1)
            st.session_state.waiting_for = 1
        else:
            try:
                number = float(cleaned_choice)
            except ValueError:
                number = None

            if number is not None:
                st.session_state.calculator_number = number
                bot_response = "Choose plus, minus, multiply, or divide."
                st.session_state.waiting_for = 3
            elif cleaned_choice in ifn.greet:
                bot_response = f"Hi {st.session_state.username}!"
            elif cleaned_choice in ifn.name:
                bot_response = random.choice(resp.name)
            elif cleaned_choice in ifn.sensored:
                bot_response = random.choice(resp.sensored)
            elif cleaned_choice in ifn.question_start:
                bot_response = random.choice(resp.question2)
                st.session_state.waiting_for = 2
            elif cleaned_choice in ifn.gay:
                bot_response = random.choice(resp.gay)
            elif cleaned_choice in ifn.joke:
                bot_response = random.choice(resp.joke)
            elif cleaned_choice in ifn.exit:
                bot_response = random.choice(resp.goodbye)
            else:
                bot_response = random.choice(resp.invalid)

    # Display bot response in chat
    with st.chat_message("assistant", avatar=assistant_icon):
        st.write(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})