def f(attack, defence, hp):
    if [False for i in (attack, defence, hp) if i < 0 or i > 15]:
        print("Invalid")
    else:
        print((attack + defence + hp) / 0.45)
f(15, 16, 0)
