# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:27:35 2023

@author: user
"""

import pandas as pd
df = pd.read_csv('tubedata.csv', header=None)
df.head()

from collections import defaultdict
station_dict = defaultdict(list)
zone_dict = defaultdict(set)

# get data row by row
for index, row in df.iterrows():
    start_station = row[0]
    end_station = row[1]
    line = row[2]
    act_cost = int(row[3])
    zone1 = row[4]
    zone2 = row[5]
    
    # station dictionary of child station tuples
    # (child_name, cost from parent to the child, tube line)
    # {"Mile End": [("Stratford", 2, "Central"), ("Wembley", 1, "Bakerloo")]}
    station_list = station_dict[start_station]
    station_list.append((end_station, act_cost, line))
    
    # the following two lines add the other direction of the tube "step"
    station_list = station_dict[end_station]
    station_list.append((start_station, act_cost, line))
    
    # we add the main zone
    zone_dict[start_station].add(zone1)
    
    # we add the secondary zone
    if zone2 != "0":
        zone_dict[start_station].add(zone2)
    
        # if the secondary zone is not 0 it’s the main zone for the ending station
        zone_dict[end_station].add(zone2)
    
    else:
        # otherwise the main zone for the ending station
        # is the same as for the starting station
        zone_dict[end_station].add(zone1)
        
        
        
        
def depth_first_search(tube_map, initial, goal, compute_exploration_cost=True, reverse=False):

    if initial == goal: # just in case, because now we are checking the children
        print("That's the same station.")
        return None
    
    # Define vars, including LIFO frontier queue
    number_of_explored_nodes = 0
    frontier = [{'station':initial, 'parent_station':None, 'time_cost':0}]
    
    explored = {initial}
    path = []

    while frontier:
        # Extract node from end of queue, LIFO
        node = frontier.pop()
        number_of_explored_nodes += 1
        
        # Checks if current node is goal
        if node['station'] == goal:
            
            # Outputs nodes explored if compute_exploration_cost is TRUE
            if compute_exploration_cost:
                print('number of explorations = {}'.format(number_of_explored_nodes))
            
            # Backtracks the path from goal to the start
            current_node = node
            total_time = 0
            while current_node is not None:     
                
                # Total Time                
                total_time += current_node['time_cost']
                # Retrace steps and add to path
                path.insert(0, current_node['station'])
                current_node = current_node['parent_station']
            
            # Print and return path from initial station to goal
            print("Path from ", initial, " to ", goal, ":\n", path)
            print("Total Travel Time:", total_time)
            return path
        
        # Creates a list of connected stations for the current station
        if not reverse:
            neighbours = tube_map.get(node['station'], []) 
        else:
            neighbours = tube_map.get(node['station'], [])
            neighbours.reverse()
        
        # Loops though all child nodes and adds them to the LIFO stack
        for child_station in neighbours:
            
            child = {'station':child_station, 'parent_station':node, 'time_cost':child_station[1]}
            
            if child_station not in explored:
                
                # LIFO queue
                new_node = {'station':child['station'][0], 'parent_station':node, 'time_cost':child_station[1]}
                frontier.append(new_node)
                explored.add(child_station)
    
    print("No Path Found")
    return None


def breadth_first_search(tube_map, initial, goal, compute_exploration_cost=True, reverse=False):

    if initial == goal: # just in case, because now we are checking the children
        print("That's the same station.")
        return None
    
    # Variable definitions and FIFO queue
    number_of_explored_nodes = 0
    frontier = [{'station':initial, 'parent_station':None, 'time_cost':0}]
    explored = {initial}
    path = []

    while frontier:
        # Extract node from end of queue, FIFO
        node = frontier.pop()
        number_of_explored_nodes += 1
        
        # Checks if current node is goal
        if node['station'] == goal:
            
            # Outputs nodes explored if compute_exploration_cost is TRUE
            if compute_exploration_cost:
                print('number of explorations = {}'.format(number_of_explored_nodes))
            
            # Backtracks the path from goal to the start
            current_node = node
            total_time = 0
            while current_node is not None:

                # Total Time                
                total_time += current_node['time_cost']
                # Retrace steps and add to path
                path.insert(0, current_node['station'])
                current_node = current_node['parent_station']
            
            # Print and return path from initial station to goal
            print("Path from ", initial, " to ", goal, ":\n", path)
            print("Total Travel Time:", total_time)
            return path
        
        # Creates a list of connected stations for the current station
        if not reverse:
            neighbours = tube_map.get(node['station'], []) 
        else:
            neighbours = tube_map.get(node['station'], [])
            neighbours.reverse()
        
        # Loops though all child nodes and adds them to the FIFO queue
        for child_station in neighbours:
            
            child = {'station':child_station, 'parent_station':node, 'time_cost':child_station[1]}
            
            
            if child_station not in explored:
                
                # FIFO queue
                new_node = {'station':child['station'][0], 'parent_station':node, 'time_cost':child_station[1]}
                frontier.insert(0, new_node)
                explored.add(child_station)
    
    print("No Path Found")
    return None


    
def uniform_cost(tube_map, initial, goal, compute_exploration_cost=True, reverse=False):

    if initial == goal: # just in case, because now we are checking the children
        print("That's the same station.")
        return None
    
    # Variable definitions and FIFO queue
    number_of_explored_nodes = 0
    frontier = [{'station':initial, 'parent_station':None, 'time_cost':0}]
    explored = {initial}
    path = []
    
    while frontier:
        # Extract node from end of queue, FIFO
        node = frontier.pop()
        number_of_explored_nodes += 1
        
        # Checks if current node is goal
        if node['station'] == goal:
            
            # Outputs nodes explored if compute_exploration_cost is TRUE
            if compute_exploration_cost:
                print('number of explorations = {}'.format(number_of_explored_nodes))
            
            # Backtracks the path from goal to the start
            current_node = node
            total_time = 0
            while current_node is not None:

                # Total Time                
                total_time += current_node['time_cost']
                # Retrace steps and add to path
                path.insert(0, current_node['station'])
                current_node = current_node['parent_station']
            
            # Print and return path from initial station to goal
            print("Path from ", initial, " to ", goal, ":\n", path)
            print("Total Travel Time:", total_time)
            return path
        
        
        
        
        # Creates a list of connected stations for the current station
        if not reverse:
            neighbours = tube_map.get(node['station'], []) 
        else:
            neighbours = tube_map.get(node['station'], [])
            neighbours.reverse()
        
        
        
        # Loops though all child nodes and adds them to the FIFO queue
        for child_station in neighbours:
            
            cost = child_station[1]
            
            # Defines current child node
            child = {'station':child_station, 'parent_station':node, 'time_cost':child_station[1]}
            
            # Makes sure node hasnt already been explored.
            if child_station not in explored:
                
                new_node = {'station':child['station'][0], 'parent_station':node, 'time_cost':child_station[1]}
                inserted = False
                
                # Loops through frontier nodes
                for i in range(len(frontier)):
                    
                    # Cost comparison
                    if cost > frontier[i]['time_cost']:
                        
                        # Inserts the node where its cost is lower than current frontier node
                        frontier.insert(i, new_node)
                        explored.add(child_station)
                        inserted = True
                        break
                
                # Checks to see if cost is still greater than others in frontier, then adds to end of queue
                if not inserted:
                    frontier.append(new_node)
                    explored.add(child_station)
    
    print("No Path Found")
    return None



def adjusted_uniform_cost(tube_map, initial, goal, compute_exploration_cost=True, reverse=False):

    if initial == goal: # just in case, because now we are checking the children
        print("That's the same station.")
        return None
    
    # Variable definitions and FIFO queue
    number_of_explored_nodes = 0
    frontier = [{'station':initial, 'parent_station':None, 'time_cost':0, 'line':None}]
    explored = {initial}
    path = []
    
    while frontier:
        # Extract node from end of queue, FIFO
        node = frontier.pop()
        number_of_explored_nodes += 1
        
        # Checks if current node is goal
        if node['station'] == goal:
            
            # Outputs nodes explored if compute_exploration_cost is TRUE
            if compute_exploration_cost:
                print('number of explorations = {}'.format(number_of_explored_nodes))
            
            # Backtracks the path from goal to the start
            current_node = node
            total_time = 0
            while current_node is not None:

                # Total Time                
                total_time += current_node['time_cost']
                # Retrace steps and add to path
                path.insert(0, current_node['station'])
                current_node = current_node['parent_station']
            
            # Print and return path from initial station to goal
            print("Path from ", initial, " to ", goal, ":\n", path)
            print("Total Travel Time:", total_time)
            return path
        
        # Creates a list of connected stations for the current station
        neighbours = tube_map.get(node['station'], []) if not reverse else []
        
        # Loops though all child nodes and adds them to the FIFO queue
        
        
        for child_station in neighbours:
            
            child_cost = child_station[1]
            
            # Defines current child node
            child = {'station':child_station, 'parent_station':node, 'time_cost':child_station[1], 'line': child_station[2]}
            
            # Makes sure node hasnt already been explored.
            if child_station not in explored:
                
                new_node = {'station':child['station'][0], 'parent_station':node, 'time_cost':child_station[1], 'line':child_station[2]}
                inserted = False
                
                # Loops through frontier nodes
                for i in range(len(frontier)):
                    
                    # Checks if a line has been changed
                    parent_line = node['line']
                    child_line = child_station[2]
                    
                    if parent_line == child_line:
                        penalty = 0
                    elif parent_line == None:
                        penalty = 0
                    else:
                        penalty = 2
                    
                    # Penalty added
                    child_cost += penalty
                    
                    if child_cost > frontier[i]['time_cost']:
                        
                        # Inserts the node where its cost is lower than current frontier node
                        frontier.insert(i, new_node)
                        explored.add(child_station)
                        inserted = True
                        break
                
                # Checks to see if cost is still greater than others in frontier, then adds to end of queue
                if not inserted:
                    frontier.append(new_node)
                    explored.add(child_station)
    
    print("No Path Found")
    return None


def best_first_search(tube_map, zone_d, initial, goal, compute_exploration_cost=True, reverse=False):

    if initial == goal: # just in case, because now we are checking the children
        print("That's the same station.")
        return None
    
    # Variable definitions and FIFO queue
    number_of_explored_nodes = 0
    frontier = [{'station':initial, 'parent_station':None, 'time_cost':0, 'line':None, 'heuristic':0}]
    explored = {initial}
    path = []
    
    while frontier:
        # Extract node from end of queue, FIFO
        node = frontier.pop()
        number_of_explored_nodes += 1
        
        # Checks if current node is goal
        if node['station'] == goal:
            
            # Outputs nodes explored if compute_exploration_cost is TRUE
            if compute_exploration_cost:
                print('number of explorations = {}'.format(number_of_explored_nodes))
            
            # Backtracks the path from goal to the start
            current_node = node
            total_time = 0
            while current_node is not None:

                # Total Time                
                total_time += current_node['time_cost']
                # Retrace steps and add to path
                path.insert(0, current_node['station'])
                current_node = current_node['parent_station']
            
            # Print and return path from initial station to goal
            print("Path from ", initial, " to ", goal, ":\n", path)
            print("Total Travel Time:", total_time)
            return path
        
        # Creates a list of connected stations for the current station
        
        
        if not reverse:
            neighbours = tube_map.get(node['station'], []) 
        else:
            neighbours = tube_map.get(node['station'], [])
            neighbours.reverse()
        
        # Loops though all child nodes and adds them to the FIFO queue
        
        
        for child_station in neighbours:
            
            child_cost = child_station[1]
            
            # Defines current child node
            child = {'station':child_station, 'parent_station':node, 'time_cost':child_station[1], 'line': child_station[2]}
            
            # Makes sure node hasnt already been explored.
            if child_station not in explored:
                
                new_node = {'station':child['station'][0], 'parent_station':node, 'time_cost':child_station[1], 'line':child_station[2], 'heuristic':0}
                inserted = False
                
                # Loops through frontier nodes
                for i in range(len(frontier)):
                    
                    # Heuristic Function
                    # Fetch Sets
                    initial_zone = zone_d[initial]
                    goal_zone = zone_d[goal]
                    child_zone = zone_d[child_station[0]]
                    
                    # Call heuristic function
                    heuristic = heuristic_func(initial_zone, child_zone, goal_zone)
                    
                    new_node['heuristic'] = heuristic
                    
                    # Cost check
                    if heuristic > frontier[i]['heuristic']:
                        
                        # Inserts the node where its cost is lower than current frontier node
                        frontier.insert(i, new_node)
                        explored.add(child_station)
                        inserted = True
                        break
                
                # Checks to see if cost is still greater than others in frontier, then adds to end of queue
                if not inserted:
                    frontier.append(new_node)
                    explored.add(child_station)
    
    print("No Path Found")
    return None

def zone_set_extractor(zone_set):
    
    # For sets with 2 values, fetches value and defines child_zone1, zone2 left "empty" with 0
    if len(zone_set) == 1:
        # Extracts values from set and adds to list
        zone_list = []
        for i in zone_set:
            
            # Converts letters to zone numbers
            if i == "a":
                i = 7
            elif i == "b":
                i = 8
            elif i == "c":
                i = 8
            elif i == "d":
                i = 9
                
            zone_list.append(int(i))
            
        zone_list.append(0)
        
        return zone_list
    
    # For sets with 2 values, fetches values
    else:
        
        # Extracts values from set and adds to list
        zone_list = []
        for i in zone_set:
            
            # Converts letters to zone numbers
            if i == "a":
                i = 7
            elif i == "b":
                i = 8
            elif i == "c":
                i = 8
            elif i == "d":
                i = 9
            
            zone_list.append(int(i))
        
        return zone_list        

def heuristic_func(initial, child_zone, goal):
    
    # Fetch initial
    initial_zone_list = zone_set_extractor(initial)
    initial_zone = initial_zone_list[0]
    
    # Fetch goal
    goal_zone_list = zone_set_extractor(goal)
    goal_zone = goal_zone_list[0]
    
    # Defines child zones
    child_zone_list = zone_set_extractor(child_zone)
    child_zone1 = child_zone_list[0]
    child_zone2 = child_zone_list[1]
    
    # When direction is positive, heading from lower to higher zone (eg. zone 5 to zone 2)
    # When direction is negative, heading from higher to lower zone (eg. zone 2 to zone 5)
    direction = initial_zone - goal_zone
    
    # Checks if in the same zone
    if child_zone1 == goal_zone:
        heuristic_cost = 0
        return heuristic_cost
    
    elif child_zone2 == goal_zone:
        heuristic_cost = 0
        return heuristic_cost
    
    # Checks if search direction is from inner to outter (1 to 9)
    # Positive direction
    if direction > 0:
        
        # checks if child zone is further out than goal zone (9 to 5)
        # outter to inner
        if child_zone1 > goal_zone:
            # Heuristic
            heuristic_cost = abs(goal_zone - child_zone1)
            return heuristic_cost
        
        # Checks if child zone is in an inner zone, (1 to 9)
        # inner to outter
        elif child_zone1 < goal_zone:
            # Heuristic
            heuristic_cost = 0
            return  heuristic_cost
    
    # Checks if search direction is negative (9 to 1)
    # Negative Direction
    elif direction < 0:
        
        # checks if child zone is further out than goal zone (9 to 1)
        # outter to inner
        if child_zone1 > goal_zone:
            # Heuristic
            heuristic_cost = 0
            return heuristic_cost
        
        # Checks if child zone is in an inner zone, (1 to 9)
        # inner to outter
        elif child_zone1 < goal_zone:
            # Heuristic
            heuristic_cost = abs(goal_zone - child_zone1)
            return  heuristic_cost
    

print("Breafth First Search:")
breadth_first_search(station_dict, "Epping", "Euston")

print("\nDepth First Search:")
depth_first_search(station_dict, "Epping", "Euston")

print("\nUniform Cost Search:")
uniform_cost(station_dict, "King's Cross St. Pancras", "Stratford")

print("\nAdjusted Uniform Cost Search:")
adjusted_uniform_cost(station_dict, "King's Cross St. Pancras", "Stratford")

print("\nBest First Search:")
best_first_search(station_dict, zone_dict, "Epping", "Liverpool Street")
