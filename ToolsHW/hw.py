import webbrowser, sys, time, random, os  

def input_math():
    try:
        while True:
            user_input = input("1 times 1 = ? ")
            if user_input == 1: 
                print(1)
                break
            elif user_input == "exit":
                sys.exit()
            else:
                print("Wrong! Try again.")
    except:
        pass 

input_math()