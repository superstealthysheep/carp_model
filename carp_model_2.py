import networkx as nx
reproductive_constant = .01
r = 2

#((2*m*c)^2)


class Lake:
  def __init__(self, value, carrying_capacity, population):
    self.value = value
    self.carrying_capacity = carrying_capacity
    self.population = population

  def reproduce(self):
    m = (r-1)/self.carrying_capacity

    self.population = (r - m * self.population) * self.population

  def __repr__(self):
    return {"value" : self.value,
            "carrying_capacity" : self.carrying_capacity,
            "population" : self.population}
  
  def __str__(self):
    return "Value: {}, Carrying Cap: {}, Population: {}".format(self.value, self.carrying_capacity, self.population)

  def spread():
    

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


