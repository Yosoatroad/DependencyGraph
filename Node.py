import copy

class NodeBuilder:

	@staticmethod
	def cook_dependency(dep_dict):
		
		def convert_node_to_str_dict(dep_dict):
			'''
			
			'''
			str_dict = {}
			for key in dep_dict:
				node = dep_dict[key]
				print key
				print node
				str_dict[key] = set([   p.name() for p in node.get_parents()  ])
			
			return str_dict
			
		def check_orphans(node_key, dep_dict):
			rest = list()
			for ky in dep_dict:
				if node_key in dep_dict[ky]:
					dep_dict[ky].remove(node_key)
					if len(dep_dict[ky]) == 0:
						rest.append(ky)

			return rest
			
		def create_update_node(node_id, node_dict):
			nodes_dependess = [ node_dict[keyee] for keyee in node_dict[node_id] ]
			new_node = Node(node_id, nodes_dependess)
			node_dict[node_id] = new_node
			
			return new_node
			
		'''
		Input: a node dependency dict with redundant dependency. For example: {A -> [B, C], B -> [C]}. A has a redundant dependency A -> C.
		Return: a node dependency dict without redundant dependency. For example: {A -> [B], B -> [C]}
		'''
		
		node_dict = {}
		for i in dep_dict:
			node_dict[i] = copy.copy(dep_dict[i])
		
		orphan_nodes = [ node_key for node_key in dep_dict if len(dep_dict[node_key]) == 0]
		for orhpan in orphan_nodes:
			dep_dict.pop(orhpan)
			
		while len(orphan_nodes) > 0:
			newbee = orphan_nodes.pop()
			
			create_update_node(newbee, node_dict)
			new_orphans = check_orphans(newbee,dep_dict)
			
			for orphan in new_orphans:
				orphan_nodes.append(orphan)
				dep_dict.pop(orphan)
		print node_dict
		return convert_node_to_str_dict(node_dict)

class Node(object):
	
	def __init__(self, id, nodes):
		'''
		id: node name 
		nodes: this node that depends on.
		If there is ancestor relationship in nodes, the older ancestor is removed and child is kept.
		So, self._parent have no common ancestor.
		'''
		
		self._id = id
		self._parent = []
		self.update_parents(nodes)
	
	def name(self):
		#str = "%s -> [%s]\n" % (self._id,  ", ".join( [ p._id for p in self._parent ] ))
		return self._id 
	
	def update_parents(self, target_to_nodes):
		'''
		Add point to nodes: this -> target_to_nodes
		
		'''
		def check_is_ancestor(node, others):
			for o in others:
				if o != node and o.is_child_of(node): # if not itself and be one of ancestor in lists, return True
					#print "Checking: %s is ancestor of %s.\n" % (node._id, o._id)
					return True
			return False
		
		def merge(old, new):
			li = list()
			li.extend(old)
			for newee  in new:
				if newee not in li:
					li.append(newee)
			return li
			
		#I have to take care of the situation of what-if ._parent is not empty
		target_to_nodes = merge(self._parent, target_to_nodes)

		parents_pool = copy.copy(target_to_nodes)
		
		for node in target_to_nodes:
			#if node is the ancestor of another node, it is removed from the list.
			if check_is_ancestor(node, parents_pool):
				parents_pool.remove(node) 
		#print  "After: %s -> [%s]\n" % (self._id,  ", ".join( [ p._id for p in parents_pool ] ))
		self._parent = parents_pool
	
	def get_parents(self):
		#return this' direct parents. And parents have no ancestor relationship.
		return self._parent
	
	def is_child_of(self, nodee):
		'''
		Checking whether nodee is this's ancestor, inculding parent relationship. 
		breath first iterating
		'''
		for parent in self._parent:
			if nodee == parent:
				return True
		
		for parent in self._parent:
			if parent.is_child_of(nodee):
				return True
		
		return False
