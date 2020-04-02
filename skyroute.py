from graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices, landmark_string
import helpers

stations_under_construction = ['Marine Drive', 'Templeton', "Main Street"]


def new_route(start_point=None, end_point=None): 
  start_point, end_point = set_start_and_end(start_point, end_point)    # Gets user inputted start and endpoint from set_start_and_end()
  if start_point == "admin":
    print("***Admin Console***\n")
    admin_console()
    return skyroute()
  elif start_point == end_point:
    print("Start point and end point must be different.\n")
  else:
    shortest_route = get_route(start_point, end_point)                    # Gets shortest route from start_point to end_point from get_route()
    if shortest_route:                                                    # get_route returns a result
      shortest_route_string = '\n'.join(shortest_route)                   # present list of results in readable format
      print("The shortest metro route from {0} to {1} is:\n\n{2}\n".format(start_point, end_point, shortest_route_string))
    else:                                                                 # get_route returns None
      print("Unfortunately, there is currently no path between {0} and {1} due to maintenance.".format(start_point, end_point))
  again = input("Would you like to see another route? Enter y/n: ")     # handles repeat request
  while again not in ['y', 'n']:
    again = input("Enter 'y' or 'n': ")
  if again == "y":                                                       
    helpers.show_landmarks(landmark_string)    
    new_route(start_point, end_point)
  elif again == "n":
    return


def set_start_and_end(start_point, end_point):  # returns startpoint and endpoint 
  if start_point != None:                                               # if repeat request
    change_point = input("What would you like to change? You can enter 'o' for 'origin', 'd' for 'destination', or 'b' for both: ")
    if change_point == 'b':
      start_point = get_start()
      end_point = None if start_point == "admin" else get_end()
    elif change_point == 'o':
      start_point = get_start()
    elif change_point == 'd':
      end_point = get_end()
    else:
      print("Oops, that isn't 'o', 'd', or 'b'...")
      return set_start_and_end(start_point, end_point)
  else:                                                                 # if initial request
    start_point = get_start()
    end_point = None if start_point == "admin" else get_end()
  return start_point, end_point

def get_start():  # gets startpoint from user input
  start_point_letter = input("Where are you coming from? Type in the corresponding letter: ")
  if start_point_letter in landmark_choices.keys():
    start_point = landmark_choices[start_point_letter]
    print("Start point: {0}\n".format(start_point))
    return start_point
  elif start_point_letter == "admin":
    return "admin"
  else:
    print("Sorry, that's not a landmark we have data on. Let's try this again...")
    return get_start()
  
def get_end():  # gets endpoint from user input
  end_point_letter = input("Ok, where are you headed? Type in the corresponding letter: ")
  if end_point_letter in landmark_choices.keys():
    end_point = landmark_choices[end_point_letter]
    print("End point: {0}\n".format(end_point))
    return end_point
  else:
    return get_end()

def admin_console():
  choice = input("Enter 'a' to add station to maintenance list, 'b' to remove station from maintenance list, 'c' to view maintenance list, or 'q' to quit: ")
  while choice not in ['a', 'b', 'c', 'q']:
    choice = input("Enter 'a', 'b' or 'c': ")
  if choice == 'a':
    station_under_construction = input("Enter station name: ")
    while station_under_construction not in vc_metro.keys() and station_under_construction != 'q':
      station_under_construction = input("Station not found. Try again: ")
    if station_under_construction == 'q':
      print("Leaving admin console. \n")
      return
    stations_under_construction.append(station_under_construction)
    print("{0} added to maintenance list.\n".format(station_under_construction))
  
  elif choice == 'b':
    print("The following stations are closed for maintenance:\n")
    for station in stations_under_construction:
      print(station)
    station_reopened = input("\nEnter station to remove from list: ")
    while station_reopened not in vc_metro.keys() and station_reopened not in stations_under_construction and station_reopened != 'q':
      station_reopened = input("Station not found. Try again: ")
    if station_reopened == 'q':
      print("Leaving admin console. \n")
      return
    stations_under_construction.remove(station_reopened)
    print("{0} removed from maintenance list.\n".format(station_reopened))
  
  elif choice == 'c':
    if stations_under_construction:
      print("The following stations are closed for maintenance:\n")
      for station in stations_under_construction:
        print(station)
    else:
      print("There are no stations closed for maintenance.\n")

  elif choice == 'q':
    print("Leaving admin console. \n")
    return
    
  again = input("Would you like to add or remove any more stations? (y/n): ")
  while again not in ['y', 'n']:
    again = input("Enter 'y' or 'n': ")
  if again == 'y':
    admin_console()
  if again == 'n':
    return

def get_route(start_point, end_point):
  start_stations = vc_landmarks[start_point]  # retrieves list of stations corresponding to startpoint
  end_stations = vc_landmarks[end_point]      # retrieves list of stations corresponding to endpoint
  routes = []
  for start_station in start_stations:
    for end_station in end_stations:
      metro_system = get_active_stations() if stations_under_construction else vc_metro # set metro_system to graph of all open stations
      if stations_under_construction:
        possible_route = dfs(metro_system, start_station, end_station) # check if a route exists
        if possible_route == []:
          return None
      route = bfs(metro_system, start_station, end_station)
      if route:
        routes.append(route)
  shortest_route = min(routes, key=len) if routes else None
  return shortest_route

def get_active_stations():                    # returns graph of available stations
  updated_metro = vc_metro
  for station_under_construction in stations_under_construction:
    for current_station, neighbouring_stations in vc_metro.items():
      if current_station != station_under_construction: # remove any references to closed stations
        updated_metro[current_station] -= set(stations_under_construction)
      else:                                   # if station closed, remove all connections
        updated_metro[current_station] = set([])
  return updated_metro


  

    


def skyroute():
  helpers.greet(landmark_string)
  new_route()
  helpers.goodbye()
  

skyroute()