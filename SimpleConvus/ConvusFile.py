import random 
from SimpleConvus import responses as resp

waiting_for_answer1 = False
waiting_for_answer2 = False

print("=======================================")
print("write exit to exit.")
print("=======================================")

while True:
    choice1 = input(": ").lower().strip()
    print("                                                ")

    if waiting_for_answer:
        print(random.choice(resp.followup2))
        print("===========================")
        waiting_for_answer = False
        continue

    for sign in ["!", "?", ".", ",", "-"]:
        choice1 = choice1.replace(sign, "")

    if choice1 == "awesome":
        print("Awesome!")
        print("==========================")
        continue
    elif choice1 in ("good", "im doing good", "im good", "good!", "awesome"):
        print(random.choice(resp.followup1))
        print("==========================")
        continue
    elif choice1 in ("how are you", "how are you doing", "how are you?", "how are you doing?"):
        print(random.choice(resp.question1))
        print("==========================")
        continue
    elif choice1 in ("hello", "hi", "sup", "whats up"):
        print(random.choice(resp.greet))
        print("==========================")
        continue
    elif choice1 == (""):
        print(random.choice(resp.question2))
        print("==========================")
        waiting_for_answer = True
    elif choice1 in ("tell me a joke", "tell a joke", "give me a joke", "joke"):
        print(random.choice(resp.joke))
        print("==========================")
        continue
    elif choice1 == "exit":
        break
    else:
        print("invalid choice")
        print("==========================")
        continue

