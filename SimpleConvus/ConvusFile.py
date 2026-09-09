import random
import responses as resp

waiting_for_answer1 = False
waiting_for_answer2 = False

print("=======================================")
print("write exit to exit.")
print("=======================================")

while True:
    choice = input(": ").lower().strip()
    print("                                                                     ")

    if waiting_for_answer2:
        print(random.choice(resp.followup2))
        print("===========================")
        waiting_for_answer2 = False
        continue
    if waiting_for_answer1:
        print(random.choice(resp.followup1))
        print("===========================")
        waiting_for_answer1 = False
        continue
    for sign in ["!", "?", ".", ",", "-"]:
        choice = choice.replace(sign, "")

    if choice in resp.special_word:
        print(resp.special_word_resp)
        print("==========================")
        continue
    elif choice in ("how are you", "how are you doing", "how are you?", "how are you doing?"):
        print(random.choice(resp.question1))
        print("==========================")
        waiting_for_answer1 = True
        continue
    elif choice in ("hello", "hi", "sup", "whats up"):
        print(random.choice(resp.greet))
        print("==========================")
        continue
    elif choice == (""):
        print(random.choice(resp.question2))
        print("==========================")
        waiting_for_answer2 = True
    elif choice in ("tell me a joke", "tell a joke", "give me a joke", "joke"):
        print(random.choice(resp.joke))
        print("==========================")
        continue
    elif choice == "exit":
        print(random.choice(resp.goodbye))
        break
    else:
        print(random.choice(resp.invalid))
        print("==========================")
        continue

