## Exercise 1

For the first exercise we had to create a graph whose nodes are authors, and two nodes are connected if they share, at least, one publication. Each edge is weighted in the following way: w(a1, a2) = 1 - J(p1, p2). Where J(p1, p2) is the Jaccard similarity between the set of publications p1 and p2 of each author.

The resulting graph (when using the full dataset) is a disconnected graph with a total of 904664 nodes and 3679331 edges. The implication of being a disconnected graph is that not all nodes are reachable from every other node, meaning, for a specific pair of nodes n1 and n2, there might not be a path that connects n1 and n2. Moreover, if the weight of the edge, w(a1, a2), between a1 and a2 is equal to 0 it means that nodes a1 and a2 only published between each other.

# Exercise 2

## Letter A

For this exercise we had to return the induced subgraph by the set of authors who published at a specific conference at least once. After creating the graph we analyse some centralities measures (degree, closeness and betweennes).

Let's check the results for conference 'any conference here' and visualize each centrality.

### Degree

### Closeness

### Betweennes 

## Letter B

On this exercise we had to get the subgraph induced by the nodes that have hop distance at most equal to a given integer, with a given author.

We observe two things:
    
    1. Because the graph is not connected we can never get the whole graph, even for a big hop distance.
    2. For a small number (between 6 and 10) of maximum hop distance we get almost the whole connected component for one author.

Let's see the behaviour observed on 2.

For author who has id = 256176 (Aris Anagnostopoulos), the connected component has 792279 nodes, if we try with maximum hop distance from 0 to 10 we have the following result.

![](plots/2_b_percentage_component.png)

Just to illustrate we show the graph for when maximum hop distance is equal to 2.

![](plots/2_b_percentage_component.png)

# Exercise 3

## Letter A

For this exercise we had to find the shortest path between Aris and a given author. To solve this problem we implemented Dijkstra's algorithm to find the shortest path.

Below we show some results.

It is important to notice that Aris is not connected to all the authors, so for some authors there will not be a shortest path between them and Aris.

## Letter B