global connections_set
connections_set = set()

class Lake:
	def __init__(self, lake_id, value, connections=set(), carpy=False):
		self.lake_id = lake_id
		self.value = value
		self.carpy = carpy
		self.connections = connections
		
	def add_connection(self, connecting_lake, blocking_cost=100): #connecting_lake is the Lake object that will be connected to self
		#the connection between the two lakes is added to the global connections_set
		new_connection = Connection(self, connecting_lake, blocking_cost)
		connections_set.add(new_connection)
		
		#the two lakes add each other to their connections set
		self.connections.add(connecting_lake)
		connecting_lake.connections.add(self)
		
class Connection:
	def __init__(self, lakes, blocking_cost=100):
		self.lakes = lakes #lakes is a frozen set containing the two lakes the connection connects
		self.blocking_cost = blocking_cost #blocking_cost is the cost associated with blocking the connection (as in preventing carp from getting through)
		
		
l1 = Lake(1, 100)
l2 = Lake(2, 50)
