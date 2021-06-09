# Knight's Tour Puzzle
 
This program was made as part of the JetBrains Academy course for Python Developers. This is the second project finished so far and uses no Object Oriented Programming. I am looking forward to revisit this engagement and solve it using OOP. Probably will be more elegant than this first approach.

The program solves the classical Knight's Tour Puzzle. Given a board of dimensions width * height (provided by the user in a CLI) a knight is placed onto the board at position (col, row) with 1 <= col <= width and 1 <= row <= height. Is it possible by legitimate moves of the knight to visit all squares of the board only once.

Either a user can try to solve the Puzzle or you can have the program generate a solution. The program tries to find a solution using Warnsdorff's heuristic when exploring all possible moves from a current position. If a solution cannot be found from the current position the program uses backtracking to explore other possibilities.
