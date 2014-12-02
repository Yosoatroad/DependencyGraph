from DependencyGraph import DependencyGraph
from Node import Node, NodeBuilder
from collections import defaultdict


def generate_dependency_graph(title, raw_graph_dependency, graph_save_path):
	'''
	@param title: String, a graph name
	@param raw_graph_dependency: dict{child:String : [parent1:String, parent2:String]}
	@param graph_save_path: String 
	@return save .jpg in graph_save_path
	'''
	
	#print branches_dependencies
	cooked_branches_dependencies = NodeBuilder.cook_dependency(raw_graph_dependency)

	print cooked_branches_dependencies
	graph = DependencyGraph(title, cooked_branches_dependencies)
	graph.create_graph(graph_save_path)
	
		
if __name__ == '__main__':
	title = "Colin Dependency Graph"
	raw_graph_dependency = {'a' : ['b','c'], 'b' : ['c'], 'c' : []}
	graph_save_path = "/var/tmp/test.jpg"
	generate_dependency_graph(title,raw_graph_dependency,graph_save_path)
