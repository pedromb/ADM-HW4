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