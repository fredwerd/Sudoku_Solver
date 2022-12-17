# Sudoku_Solver

# GUI with a 9x9 grid to input values. Includes a solve button, and a reset button
# Solve button runs the entire solving code, which employs several techniques in the following order:
1. Store given values in a 9x9 array
2. Check given values for any input errors
3. Create a storage array of all possible solutions for every unsolved box
4. Eliminates possible solutions from the storage array based on input data
5. Fills 9x9 unsolved array boxes if only one viable solutions remains
6. Fills 9x9 unsolved array boxes if they are the only possible location for a solution in any row, column, or 3x3 box
7. Brute Force solving by temporarily filling unsolved boxes one at a time and moving on until a conflict is found. 
From there, it restarts at the first filled box trying the next number and continuing along the puzzle. 


# Brute force solving exists as it's own automated solving algorithm.
# Traditionally, it begins with the assumption that every unsolved square can be every number from 1 to 9.
# This program begins with simple solving techniques to reduce the time to brute force, by producing an array that the brute force can use to skip solutions that have already been ruled out by the prior techniques.

# For the future, the solver will have added techniques, more robust warning messages regarding input errors, more proactive input error visualisation, and optimization
