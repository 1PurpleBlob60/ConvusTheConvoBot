import random
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
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.waiting_for = None
        st.session_state.calculator_number = None
        st.session_state.calculator_operator = None
        st.rerun()

# 2. Render previous chat messages on rerun
for message in st.session_state.messages:
    if message["role"] == "assistant":
        message_context = st.chat_message("assistant", avatar=assistant_icon)
    else:
        message_context = st.chat_message("user", avatar=user_icon)

    with message_context:
        st.write(message["content"])

# 3. Handle User Input
if user_input := st.chat_input("Type a message..."):
    # Display user message in chat
    with st.chat_message("user", avatar=user_icon):
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
                bot_response = random.choice(resp.greet)
            elif cleaned_choice in ifn.name:
                bot_response = random.choice(resp.name)
            elif cleaned_choice in ifn.sensored:
                bot_response = random.choice(resp.sensored)
            elif cleaned_choice in ifn.question_start:
                bot_response = random.choice(resp.question2)
                st.session_state.waiting_for = 2
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