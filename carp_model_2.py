"""
Measures carp spread from lake to lake over time
"""
#import mathplotlib.pyplot as plt
import networkx as nx
import numpy as np

r = 1

number_of_spreads_per_season = 1

class Lake:
  def __init__(self, value, carrying_capacity, population):
    self.value = value
    self.carrying_capacity = carrying_capacity
    self.population = population
    self.change_in_population = 0 #this is used for storing values from calculate_fish_spread()

  def reproduce(self):
    #uses a continuous model of logistic growth based on differential equations

    if self.population == self.carrying_capacity:
      return None #if the population is at the carrying capacity, escape the function because otherwise it will divide by zero

    c = self.population / (self.carrying_capacity - self.population)
    t = 1
    self.population = self.carrying_capacity * c * np.exp(r * t) / (1 + c * np.exp(r * t)) #as long as self.population and t are positive, c * np.exp(r * t)) should be nonzero, so dividing by zero should not be an issue.
 
  def __repr__(self):
    return str({"value" : self.value,
            "carrying_capacity" : self.carrying_capacity,
            "population" : self.population})
  
  def __str__(self):
    return "Value: {}, Carrying Cap: {}, Population: {}".format(self.value, self.carrying_capacity, self.population)

  def calculate_fish_spread(self): #calculates how much the lake's population will change when fish randomly spread but does NOT actually change the population.
    self.change_in_population = 0
    for neighbor in list(lake_graph.neighbors(self)): #for loop iterating through all of the lakes neighboring self
      #below is how many fish self will gain from its neighbors
      self.change_in_population += (neighbor.population * lake_graph.edges[neighbor, self]["passing_probability"])
      #lake_graph.edges[neighbor, self]["passing_probability"] is the passing probability of the connection between self and neighbor, i.e. the probability for a particular fish in either of the lakes to travel to the other lake

      #below is how many fish self will lose to its neighbors
      self.change_in_population += (-1 * self.population * lake_graph.edges[neighbor, self]["passing_probability"])

  def commit_fish_spread(self): #puts the population effects from calculate_fish_spread() into effect. The reason why the two parts are split apart is that, if they weren't, the first lakes' populations would change before the other lakes could calculate how their populations should change. This would throw the caluclations off and fish wouldn't be conserved anymore.
    self.population += self.change_in_population
    self.change_in_population = 0

  def calculate_effective_value(self):
    return self.value * (1 - self.population/self.carrying_capacity)

lake_graph = nx.Graph()

lake_dict = {"l1" : Lake(100, 1000, 5), 
             "l2" : Lake(50, 10, 0)}
connection_list = [(lake_dict["l1"], lake_dict["l2"], {"passing_probability": .1})]

lake_graph.add_nodes_from(lake_dict.values()) #the .values is so that the Lake objects, not the keys, are added to the lake_graph.
lake_graph.add_edges_from(connection_list)

for season in range(0, 100):
  total_effective_value = 0
  for lake in lake_graph.nodes():
    total_effective_value += lake.calculate_effective_value()

  #printing lake info
  print("Season {}".format(season))
  print("="*20)
  print("Lakes:")
  for lake in lake_graph.nodes():
    print(str(lake))
  print("Total Value: {}".format(total_effective_value))
  print("")

  #fish reproduction
  for lake in lake_graph.nodes():
    lake.reproduce()
  #fish spreading
  for i in range(0, number_of_spreads_per_season):  
    for lake in lake_graph.nodes():
      lake.calculate_fish_spread()

    for lake in lake_graph.nodes():
      lake.commit_fish_spread()

