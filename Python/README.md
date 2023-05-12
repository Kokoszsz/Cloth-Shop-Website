## Python programs ##
Simple Python programs and games mostly build using pygame library

### Installing ###
To install and run the project, follow these steps:

1. Download the Python 3 installer package from the official website and install it, if not installed on your local machine.
2. Clone the repository to your local machine.
3. Install the required packages by running ```pip install -r requirements.txt``` in your terminal.

### Chess ###
Chess is a classic two-player strategy board game. 
The objective of the game is to checkmate the opponent's king by placing it under an inescapable threat of capture.

#### To play chess: ####
1. Run chess_main.py.
2. The game will begin with the white player's turn. To move a piece, click on it with the left mouse button.
3. After clicking on a piece, the legal moves that it can make will be highlighted in green. If there are any enemy pieces that the selected piece can capture, those squares will be highlighted in red.
4. Click on the square where you want to move the selected piece. If the move is legal, the piece will move to that square.
5. If your move puts the opponent's king under attack, the opponent must respond by moving their king or by moving another piece to block the attack.
6. Take turns moving pieces until one player achieves checkmate, or until the game ends in a stalemate or draw. Then game restarts automatically 

#### Important ####
Not all rules are implemented like:
- castling
- swapping a pawn when it reaches the opposite edge
- en passant move


### Minesweeper ###
A simple minesweeper game

#### To play the game: ####
1. Run the program.
2. Choose game size
3. Choose game difficulty
4. Left-click on a cell to reveal what's underneath it.
5. Right-click on a cell to flag it as containing a mine. This can help you keep track of which cells you think are dangerous.


### Pathfinding program ###
This is a pathfinding program that uses the A\* search algorithm to find the shortest path between two points on a grid.

#### How to use: ####
1. Run the program.
2. Click on a cell to mark where the path should begin (the cell will turn orange).
3. Click on a cell to mark where the path should end (the cell will turn blue).
4. Next you can mark some remaining white cells as black to make them impassable.
5. Press the spacebar to start the search algorithm and watch the program find the shortest path.
6. When the algorithm finishes, the shortest path will be highlighted in purple cells. If there is no path, a message informing about this will be displayed.


The "clear" button erases the current grid.
The "random" button randomly arranges the cells on the grid.


### Snake ###
A simple snake game

#### To play the game: ####
1. Run the program.
2. Use the w, a, s, and d keys to move the snake up, left, down, and right, respectively.
3. Use the p key to pause and unpause the game.

The game starts with a snake consisting of a single block. 
The player must navigate the snake around the game board to collect food, which appears randomly. 
Each time the snake eats a piece of food, it grows in length. 
The game ends when the snake collides with itself or with a wall.

### Tetris ###
A simple tetris game

#### To play the game: ####
1. Run the program.
2. Use the a and d keys to move the current block left and right, respectively.
3. Use the s key to rotate the current block.
4. Use the spacebar key to immediately place the current block at the bottom of the grid.
5. Use the p key to pause and unpause the game.
6. Use the r key to restart the game.

The game starts with a random block dropping from the top of the grid. 
When a row is filled with blocks, that row disappears and the player scores points. 
The game gets faster with each score the player earns.

### Download images ###
Small program that using selenium downloads images from imgur.com. and store it in images folder (if there is no such a folder it creates on)
You can change kind of downlaoded picture by chenging 'Word_Search' variable and modyfing number of downloaded images by changing 'Number_of_pictures' variables.