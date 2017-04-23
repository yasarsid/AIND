# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The Naked Twins are 2 cells in the soduko that form a complimentary pair of possibilities. For Eg The possible values for cell A1 and A2 both can be '12'.
This implies either one of them is  1 and the other 2. We are not able to make it if 1 belongs to A1 or A2 at this point.
conversely it can be stated that if we take a intersection of all the peers of the cells A1 and A2 we can definitly say that neither of them will be 1 or 2.

So the constraint is that for a naked pair the intersection of their peers can not have either of the values.

On the road to solving the soduku,  The sudoku undergoes a regular transformation based on elimination and other techniques.
Assuming the Sudoku enters the Naked Twin Constraint Transformation with a State S1.
We can keep on applying (propagate) Naked Twins constraint on the repeatedly sudoku to weed out values and
reduce the possible solutions for the soduko. Post iterative application of this constraint the soduku transforms to a state S2,
where all Naked Twin constrained based pruning of the solution space has been done has been done.

Now the Soduku is transformed from this state S2 to other states using other techniques like elimination, only choice and DFS Search.
Each time we get a new state of the sudoku we again apply naked twin constraint.

Summing up - The Naked Twins constraint provides us with a good heuristic to reduce the run time and conditions to be evaluated.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A:
In the diagonal Sudoku problem - We have an additional contraint to satisfy along with more traditional sudoku contraints.
The Diagonal Constraint is that the elements along the diagonal from A1 to I9 and from I1 to A9 each digit from 1 to 9 can appear only once.

By evaluating this constraint we can reduce/eliminate possible solution for each cell along the diagonal.

So now when we eliminate possibilities across the a set of peers the number of cells impacted is greater
Without this constraint the peer set was only 20 now it increases to 26 for diagonal elements.

For Example if we evaluate(or if stated) A1=1 then we are sure
that a Set of 25 Elements - {'D1', 'A5', 'H8', 'D4', 'F1', 'E1', 'G7', 'A2', 'C1', 'I9', 'B2', 'I1', 'E5', 'C2', 'B1', 'G1', 'H1', 'B3', 'A9', 'A6', 'C3', 'A7', 'A3', 'F6', 'A4', 'A8'}
cannot have a value '1'. This reduces our search space ~ by a count of 25.

We repeatedly apply this constraint to the given sudoku, coupled with other techniques like DFS search, only choice we can solve the soduku.


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

