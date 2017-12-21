# ADM-HW4
Repository for Homework 4 of Algorithmic Methods for Data Mining - Group 0

From the root folder run

```
python3 homework.py -e <exercise_number> -l <exercise_letter> -r <reduced_data>
```
* Exercise number can be 2 or 3
* Exercise letter can be a or b
* Reduced can be 0 or 1

If reduced is 1 it uses the reduced dataset to create the graph, if reduced is 0 it uses the full dataset to create the graph.

Since exercise 1 is just creating the graph by running any other exercise you can actually check if the graph was created correctly. If you wish to check the graph directly create an instance of the Graph class from src/graph.py module and access the graph attribute.


### Exercise 1

In order to process the JSON files, it has been created a proper class called Graph. The instantiation of a Graph object can initialize two different processes:

- If a Graph object is not present in the folder you are working in, it start the process of creation of the whole graph starting from the JSON file.
- If a Graph object is present in the folder you are working in, then it is loaded and all the following processes will work on the loaded graph.

In the instantiation you can also specify whether you want to use the reduced file (reduced_dbsl.json) or the full file (dbsl.json) to create the graph.

If it has to create the graph, he start to parse the JSON file. Since every document is a publication, we take for each document the author(s), and for each one, if it hasn't been done yet before, it is created a node in the graph. And since every edge links two authors that at least have one publication in common, for each document are added all the possible edges between the nodes that represents the authors, obviously whether they already don't exists.

Once all the nodes and the edges were created, it computes the weights according to the Jaccard Distance, and add them to the graph.


### Exercise 2

#### Letter A

Given the conference in input, it looks up in the graph through all the authors (nodes), and saves the ones that have at least published once in the given conference. Once obtained all the nodes it needs, run the function "subgraph" of NetworkX, that returns a graph object that is nothing but the subgraph induced we were looking for.

Visualization part...

#### Letter B

Basically it starts looking for the nodes that are at maximum distance equal to the one in input. Then it run the NetworkX function "subgraph" to return the induced subgraph composed of that nodes.

In order to perform this, it uses three different variables:

- author_ids,a list where at the i-th loop contains the nodes at distance i from the root

- subgraph_ids where there are saved all the nodes from the root one to the ones at distance d.

- node_list, a nested list where i-th element is a list of the nodes at distance i to the root. It is useful to make the colors for the visualization.

Then:

1) Take the nodes connected from the root and save them in author_ids, in order to take at the next iteration their neighbors
2) Extend subgraph_ids list with author_ids.
3) Append author_ids to nodes_list.

It does this d times. Doing in this way, at the end it has in subraph_ids all the nodes it visited, and in node_list the same nodes but divided according to their distance from the root node. It creates the subgraph and returns it and node_list. Then for the visualization, we used the Fruchterman-Reingold layout, that is one of the force-directed graph drawing algorithms provided by NetworkX library. We gave different colors to the nodes, according to their distance to the root node, and the colors are given at random every time you run the program.
