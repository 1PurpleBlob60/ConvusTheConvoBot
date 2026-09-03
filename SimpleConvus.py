import random 

resp1 = ["Great", "Good to hear that", "Awesome!"]
resp2 = ["Good, you?", "I'm good, you?"]
resp3 = ["Hi There!", "Hi!", "Hello"]
resp4 = ["What do you like?", "What is you favourite food?"]
resp_followup = ["That's great!", "Wow", "Awesome"]
resp_joke = ["Why can't you tell a joke to an egg? It might crack up!", "What do you call a magic dog? A labracadabrador!"]

waiting_for_answer = False

print("=======================================")
print("write exit to exit.")
print("=======================================")

while True:
    choice1 = input(": ").lower().strip()
    print("                                                ")

    if waiting_for_answer:
        print(random.choice(resp_followup))
        print("===========================")
        waiting_for_answer = False
        continue

    for sign in ["!", "?", ".", ",", "-"]:
        choice1 = choice1.replace(sign, "")

    if choice1 == "awesome":
        print("Awesome!")
        print["=========================="]
        continue
    elif choice1 in ("good", "im doing good", "im good", "good!", "awesome"):
        print(random.choice(resp1))
        print("==========================")
        continue
    elif choice1 in ("how are you", "how are you doing", "how are you?", "how are you doing?"):
        print(random.choice(resp2))
        print("==========================")
        continue
    elif choice1 in ("hello", "hi", "sup", "whats up"):
        print(random.choice(resp3))
        print("==========================")
        continue
    elif choice1 == (""):
        print(random.choice(resp4))
        print("==========================")
        waiting_for_answer = True
    elif choice1 in ("tell me a joke", "tell a joke", "give me a joke", "joke"):
        print(random.choice(resp_joke))
        print("==========================")
        continue
    elif choice1 == "exit":
        break
    else:
        print("invalid choice")
        print("==========================")
        continue

