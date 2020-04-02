def greet(landmark_string):
  print("Hi there and welcome to SkyRoute!\n")
  print("We'll help you find the shortest route between the following Vancouver landmarks:\n\n" + landmark_string)

def goodbye():
  print("Thanks for using SkyRoute!")

def show_landmarks(landmark_string):
  print("\n")
  see_landmarks = input("Would you like to see the list of landmarks again? Enter y/n: ")
  if see_landmarks == "y":
    print("\n" + landmark_string + "\n")
  elif see_landmarks == "n":
    return
  else:
    return show_landmarks(landmark_string)