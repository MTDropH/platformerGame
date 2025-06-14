shopping = []

want = input("what do you want to get?")
while want != "0":
    shopping.append(want) 
    want = input("what do you want to get?")

if shopping <3:
    print("wow thats a big shop.you wanted...",shopping)

elif shopping >3:
    print("not much food in your trolley.you wanted",shopping)

else:
    print(shopping)
