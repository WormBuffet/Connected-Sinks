from collections import deque

# Dictionary Containing Each Pipe Character and their Respective Positions Where they can Connect to Other Pipes
PIPE_DIRECTIONS = {
    '═': [(0, 1), (0, -1)],  # Horizontal
    '║': [(1, 0), (-1, 0)],  # Vertical
    '╔': [(0, 1), (1, 0)],   # Right, Down
    '╗': [(0, -1), (1, 0)],  # Left, Down
    '╚': [(0, 1), (-1, 0)],  # Right, Up
    '╝': [(0, -1), (-1, 0)], # Left, Up
    '╠': [(0, 1), (1, 0), (-1, 0)],  # Right, Down, Up
    '╣': [(0, -1), (1, 0), (-1, 0)], # Left, Down, Up
    '╦': [(0, 1), (0, -1), (1, 0)],  # Right, Left, Down
    '╩': [(0, 1), (0, -1), (-1, 0)],  # Right, Left, Up
    ' ': [ ]
}

DIRECTIONS = [
     (0, 1), # Right
     (0, -1), # Left
     (1, 0),  # Down
     (-1, 0) # Up
]

def get_pipe_directions(char):
    return PIPE_DIRECTIONS.get(char, set()) 



def find_sinks(grid, rows, columns):
    
    # Find the Starting Position on the Grid 
    # In this Example it is the Coordinates x:34, y:17
    startingChar = '*'
    startingPosition = None
    for x in range(0, rows):
        for y in range(0, columns):
             if grid[x][y] == startingChar: 
                  startingPosition = (x, y)      
    if startingPosition == None:
        raise Exception("No Source Position in DataSet!") 

    visited = set()
    connected_sinks = set()
    queue = deque([startingPosition])
    
    # Print a Visual Diagram of the Grid
    for i in range(0, rows):
             print(*grid[i])
    
    while queue:
        row, column = queue.popleft()
        
        # If the Position has Already been Visited, Skip Over it
        if (row, column) in visited:
            continue
        visited.add((row, column))
        
        # Checking if the Current Element is a Sink (A Letter)
        if grid[row][column].isupper():
            print(grid[row][column])
            connected_sinks.add(grid[row][column])
            
        # If the current element is a Sink or the Starting Position, they can Move in all 4 Directions.
        if grid[row][column] == startingChar or grid[row][column].isupper():
            current_directions = DIRECTIONS
        else:
            current_directions = get_pipe_directions(grid[row][column])
             
        for move_row, move_column in current_directions:
             new_row, new_column = row + move_row, column + move_column
             
             if 0 <= new_row < rows and 0 <= new_column < columns and (new_row, new_column) not in visited:
                 # If New Pipe Character's Valid Connection Position Contains the Inverse of the Current Movement Position, the Two Can Connect
                 if (-move_row, -move_column) in get_pipe_directions(grid[new_row][new_column]) or grid[new_row][new_column].isupper():
                    queue.append((new_row, new_column))
                                  
    return connected_sinks
             

def import_data(dir):
    # 2D Array for Storing the Unsorted Coordinate and Pipe Data
    array2D = []  
    
    # Total Number of Rows and Columns
    rows = 0
    columns = 0

    with open(dir, encoding='utf-8-sig', newline='') as f:
            for line in f.read().splitlines(): # read file and split strings into a list
                lineArr = line.split(' ') # split each variable using a space as the delimiter
                
                tempArr = [] 
                tempArr.append(lineArr[0]) 
                for i in lineArr[1:]: # skip over first instance, as it will never be a number
                    tempArr.append(int(i))
                    
                # Determine the Maximum Value for both the Rows and Columns
                # Coordinates can have a Value of 0, so we add 1 to get the true number of Rows/Columns
                if int(lineArr[1]) > rows:
                        rows = int(lineArr[1]) + 1
                if int(lineArr[2]) > columns:
                        columns = int(lineArr[2]) + 1
                    
                array2D.append(tempArr)
     
    # Sort Array by X & Y Coordinates
    partiallySortedArray = sorted(array2D,key=lambda x: x[2])
    sortedArray = sorted(partiallySortedArray,key=lambda x: x[1])
            
    grid = [] # Main Grid 2D Array
    tempArr = []
    
    # Counter Variables
    counter = 0
    rowCounter = 0
    colCounter = 0
          
    # Converting the Sorted Array into a 2D Grid Array
    while counter < len(sortedArray):
        if rowCounter < sortedArray[counter][1]: # Once the End of a Row has been Reached, Move to the Next
            rowCounter += 1 
         
        if colCounter != sortedArray[counter][2]: # If the Column Position doesn't Exist, Make it Blank
            tempArr.append(' ')
        else:
            tempArr.append(sortedArray[counter][0]) 
            counter += 1
            
        colCounter += 1
        
        # Append the Array of "Pipe" Characters and Reset the Temporary Array and Column Counter
        if colCounter == columns:
            grid.append(tempArr)
            colCounter = 0
            tempArr = []   
          
    # Return Grid, Row, and Columns        
    return grid, rows, columns


grid, rows, columns = import_data('Sink Data/sinkData1.txt')
find_sinks(grid, rows, columns)
