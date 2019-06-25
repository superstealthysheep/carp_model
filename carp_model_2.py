"""
Measures carp spread from lake to lake over time
"""
#import mathplotlib.pyplot as plt
import networkx as nx

reproductive_constant = .01
r = 2

#((2*m*c)^2)


class Lake:
  def __init__(self, value, carrying_capacity, population):
    self.value = value
    self.carrying_capacity = carrying_capacity
    self.population = population
    self.change_in_population = 0 #this is used for storing values from calculate_fish_spread

  def reproduce(self):
    m = (r-1)/self.carrying_capacity

    self.population = (r - m * self.population) * self.population

  def __repr__(self):
    return str({"value" : self.value,
            "carrying_capacity" : self.carrying_capacity,
            "population" : self.population})
  
  def __str__(self):
    return "Value: {}, Carrying Cap: {}, Population: {}".format(self.value, self.carrying_capacity, self.population)

  def calculate_fish_spread(self): #caluclates how much the lake's population will change when fish randomly spread but does NOT actually change the population.
    change_in_population = 0
    for neighbor in list(lake_graph.neighbors(self)): #for loop iterating through all of the lakes neighboring self
      #below is how many fish self will gain from its neighbors
      self.change_in_population += (neighbor.population * lake_graph.edges[neighbor, self]["passing_probability"])
      #lake_graph.edges[neighbor, self]["passing_probability"] is the passing probability of the connection between self and neighbor, i.e. the probability for a particular fish in either of the lakes to travel to the other lake

      #below is how many fish self will lose to its neighbors
      self.change_in_population += (-1 * self.population * lake_graph.edges[neighbor, self]["passing_probability"])

  def commit_fish_spread(self): #puts the population effects from calculate_fish_spread() into effect. The reason why the two parts are split apart is that, if they weren't, the first lakes' populations would change before the other lakes could calculate how their populations should change. This would throw the caluclations off and fish wouldn't be conserved anymore.
    self.population += self.change_in_population
    self.change_in_population = 0

lake_graph = nx.Graph()

lake_list = [Lake(100, 1000, 5), Lake(50, 10, 0)]
connection_list = [(lake_list[0], lake_list[1], {"passing_probability": .01})]

lake_graph.add_nodes_from(lake_list)
lake_graph.add_edges_from(connection_list)

for season in range(0, 20):
#printing lake info
  print("Season {}".format(season))
  print("="*20)
  print("Lakes:")
  for lake in lake_graph.nodes():
    print(str(lake))

  print("")


  for lake in lake_graph.nodes():
    lake.reproduce()
    lake.calculate_fish_spread()

  for lake in lake_graph.nodes():
    lake.commit_fish_spread()


