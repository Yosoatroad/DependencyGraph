#'pyparsing', '1.5.5'. 'pydot','1.0.2'
import copy
import pydot

class DependencyGraph(object):
	
	def __init__(self, graph_title, nodes_dependencies):
		self._graph_title = graph_title
		self._nodes_dependencies = nodes_dependencies

	def create_graph(self, saved_location):
		'''
		Input: a file path
		retrun: save result 
		'''
		copied = {}
		for k in self._nodes_dependencies:
			copied[k] = copy.copy(self._nodes_dependencies[k])
		dependency_layer = self.generate_dependency_layer(copied)
		graph = self.init_pydot_graph_nodes(self._graph_title, dependency_layer)
		self.init_pydot_graph_edges(self._nodes_dependencies, graph)
		return graph.write_jpg(saved_location)
		
	def generate_dependency_layer(self, ndag, base_layer = 0, pre_removed = set(), layer_dict = dict()):
		'''
		@param: ndag: dict[branch_name, set[branch_name]()]
		@return: layer_dict[branch_name, layer:Int]
		'''
		if len(ndag) == 0:
			return layer_dict
		
		remove_list = set()
		for k in ndag:
			if ndag[k].issubset(pre_removed):
				remove_list.add(k)				
				layer_dict[k] = base_layer + 1
		for removed in remove_list:
			ndag.pop(removed)
		
		return self.generate_dependency_layer(ndag, base_layer + 1, remove_list | pre_removed, layer_dict)
		

	def init_pydot_graph_nodes(self, graph_title, branch_layer_map):
		'''
		@param branch_layer_map: dict[branch_name, layer:Int]
		@return a generated graph
		'''
		layers = max(branch_layer_map.values()) + 1
		
		graph = pydot.Dot(labelloc="t",label=graph_title, graph_type = 'digraph',ratio = "fill")
		graph.add_subgraph(pydot.Subgraph('',rank='source'))
		for i in range(1,layers - 1) :
			graph.add_subgraph(pydot.Subgraph('',rank='same'))
		graph.add_subgraph(pydot.Subgraph('',rank='sink'))
		for key in branch_layer_map.keys():
			graph.get_subgraph_list()[branch_layer_map[key]].add_node(pydot.Node(key,label = key,color='blue',shape ='box',fontsize = '9', fontname = 'Sans'))
			
		return graph
		

	def init_pydot_graph_edges(self, branches_dependencies, graph):
		'''
		@param: branches_dependencies: dict[branch_name, list[branch_name]]
		@return: Nothing, but updated graph with edges
		'''
		for child_project in branches_dependencies:
			for parent_project in branches_dependencies[child_project]:
				if child_project != parent_project:
					edge_color = 'blue'
					edge = pydot.Edge(child_project, parent_project, label='', fontsize='9', fontname='Sans', penwidth='2', arrowsize='1', color=edge_color, weight='10')
					graph.add_edge(edge)
				
