
def handleInput():
    num1 = int(input("Input first number:"))
    num2 = int(input("Input second number:"))
    operand = input("Input a valid operand(+, -, *, /, mod, ^,):")

    if operand == "+":
        print("Result is:")
        print(num1 + num2)
    elif operand == "-":
        print("Result is:")
        print(num1 - num2)
    elif operand == "*":
        print("Result is:")
        print(num1 * num2)
    elif operand == "/":
        print("Result is:")
        print(num1/num2)
    elif operand == "mod":
        print("Result is:")
        print(num1 % num2)
    elif operand == "^":
        print("Result is:")
        print(num1**num2)
    else:
        print("Invalid operand.")
    handleInput()

handleInput()