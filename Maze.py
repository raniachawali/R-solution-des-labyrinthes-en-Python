from enum import Enum
from typing import List,NamedTuple,Callable,Optional 
import random
from math import sqrt
from generic_search import dfs, bfs, node_to_path, astar, Node

class Cell(str,Enum):
    EMPTY=" "
    BLOCKED="X"
    START="S"
    GOAL ="G"
    PATH="*"

class MazeLocation(NamedTuple):
    row : int
    column : int

class Maze :
    def __init__(self,rows: int=10,columns:int =10 ,sparseness:float=0.2,start:MazeLocation=MazeLocation(0,0),goal:MazeLocation=MazeLocation(9,9)) -> None:
        #initialize basic instance variables
        self._rows: int=rows
        self._columns: int =columns
        self.start: MazeLocation=start
        self.goal : MazeLocation=goal
        #fill the grid with empty cells
        self._grid: List[List[Cell]]=[[Cell.EMPTY for c in range(columns)] for r in range(rows)]
        #populate the grid with blocked cells
        self._randomly_fill(rows,columns,sparseness)
        #fill the start and goal locations in 
        self._grid[start.row][start.column]=Cell.START
        self._grid[goal.row][goal.column]=Cell.GOAL

    def _randomly_fill(self,rows:int,columns:int, sparseness:float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0,1.0 )< sparseness:
                    self._grid[row][column]=Cell.BLOCKED
    #uses that sparseness parametre ,generates a random number between 0 
    # and 1 point oh and sees is it less than sparseness so is it 
    # less than 0.2 which means approximately 20% of the time
    # will fill the grid with the blocks location    
    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output+="".join([c.value for c in row])+"\n"
        return output
    # return a nicely formatted version of the maze for printing
    def goal_test(self,ml: MazeLocation)-> bool:
        return ml == self.goal
    # tells us if some location actually is the place that we wanted 
    # to get to 

    def successors(self,ml:MazeLocation)-> List[MazeLocation]:
        locations :List[MazeLocation]=[]
        # move one row down
        if ml.row +1 < self._rows and self._grid[ml.row +1][ml.column]!=Cell.BLOCKED:
            locations.append(MazeLocation(ml.row +1 ,ml.column))
        #move one row up
        if ml.row -1 >=0 and self._grid[ml.row -1][ml.column]!=Cell.BLOCKED:
            locations.append(MazeLocation(ml.row -1 ,ml.column))
        #move one column to the right 
        if ml.column +1 < self._columns and self._grid[ml.row][ml.column +1]!=Cell.BLOCKED:
            locations.append(MazeLocation(ml.row,ml.column+1))
        #move one column to the right
        if ml.column -1 >=0 and self._grid[ml.row][ml.column -1]!=Cell.BLOCKED:
            locations.append(MazeLocation(ml.row,ml.column-1))
        return locations

    def mark(self, path: List[MazeLocation]):
        for maze_location in path :
            self._grid[maze_location.row][maze_location.column]=Cell.PATH
        self._grid[self.start.row][self.start.column]=Cell.START
        self._grid[self.goal.row][self.goal.column]=Cell.GOAL
    # it takes a list of maze locations and fills them in with asterisks
    #and then replaces the starting goal again in case the asterisk 
    #overlaid the start ot the goal 
    def clear(self, path: List[MazeLocation]):
        for maze_location in path :
            self._grid[maze_location.row][maze_location.column]=Cell.EMPTY
        self._grid[self.start.row][self.start.column]=Cell.START
        self._grid[self.goal.row][self.goal.column]=Cell.GOAL 
    
    #teb3a DFS 
    def euclidean_distance(goal:MazeLocation)-> Callable[[MazeLocation],float]:
        def distance(ml:MazeLocation) -> float:
            xdist: int = ml.column -goal.column
            ydist : int = ml.row - goal.row
            return sqrt((xdist*xdist)+(ydist*ydist))
        return distance
    #return a fonction that given a different maze location tells us 
    # the distance to the goal which is going to a flow 
    # the second funtion dista,ce calculate the distance to the goal 



 
    # teb3a A*
def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)
        return (xdist + ydist)
    return distance

if __name__ == "__main__":
    # Test DFS
    m: Maze = Maze()
    print(m)
    solution1: Optional[Node[MazeLocation]] = dfs(m.start, m.goal_test, m.successors)
    if solution1 is None:
        print("No solution found using depth-first search!")
    else:
        path1: List[MazeLocation] = node_to_path(solution1)
        m.mark(path1)
        print(m)
        m.clear(path1)

    # Test BFS
    solution2: Optional[Node[MazeLocation]] = bfs(m.start, m.goal_test, m.successors)
    if solution2 is None:
        print("No solution found using breadth-first search!")
    else:
        path2: List[MazeLocation] = node_to_path(solution2)
        m.mark(path2)
        print(m)
        m.clear(path2)
        
    # Test A*
    distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
    solution3: Optional[Node[MazeLocation]] = astar(m.start, m.goal_test, m.successors, distance)
    if solution3 is None:
        print("No solution found using A*!")
    else:
        path3: List[MazeLocation] = node_to_path(solution3)
        m.mark(path3)
        print(m)

    
























        