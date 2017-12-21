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

- If a Graph object is \textbf{not} present in the folder you are working in, it start the process of creation of the whole graph starting from the JSON file.
- If a Graph object is present in the folder you are working in, then it is loaded and all the following processes will work on the loaded graph.

In the instantiation you can also specify whether you want to use the reduced file (reduced\_dbsl.json) or the full file (dbsl.json) to create the graph.

If it has to create the graph, he start to parse the JSON file. Since every document is a publication, we take for each document the author(s), and for each one, if it hasn't been done yet before, it is created a node in the graph. And since every edge links two authors that at least have one publication in common, for each document are added all the possible edges between the nodes that represents the authors, obviuìously whether they already don't exists.

Once all the nodes and the edges were created, it computes the weights according to the Jaccard Distance, and add them to the graph.
