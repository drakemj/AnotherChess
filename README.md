# Another Chess Project
The goal of this project is to train an AI using a camera to determine the position of a chessboard. With this function comes many different applications such as AI, connectivity with Lichess, move suggestions, etc. Though there is no real reason to reinvent the wheel and rebuild all of the chess functionality that is included in this project (such as legal move checking), it is fun. :)

## Key Functionality
The enclosed program will keep track of the board. The current state of the board as viewed by the AI will be displayed on the board. As a move is made, the screen will indicate the legality of the move. Different gamemodes can be selected via a UI.

As of right now, there is a working GUI and chess application which adheres to all of the rules. You can flip the board, play out moves, and seek through the game via the table of moves on the right as well as the seek arrows. Additionally, it currently can play against real players through Lichess using a personal access token, which will hopefully be updated to an OAuth2 Session in the future. Online functionality is still a bit buggy at times, but full games can be completed through it.

## Planned Features
- Saving your game, so that you can pick it up another time
- Time control + other settings
- Online stability
- AI recognition + online play with a physical board!

## Installation
While in the root directory, install required libraries by running

`pip install -r requirements.txt`

Then, you can run the application by running

`python3 src/AnotherChess.py`

and if things are successful, you should see the following window.
![image](https://user-images.githubusercontent.com/62521534/214699770-bfac1696-34c4-4af2-bfaf-6ed91b305884.png)

When opening the application, it is by default in analysis mode, so you can play out moves from both sides if moves are legal.

![move_demo](https://user-images.githubusercontent.com/62521534/214700944-2a4013d4-e31f-4caa-959b-2225fbe95db9.gif)

You can search through the game to get the position at a particular move, using the GUI table on the right or the seek arrows.

![search_demo](https://user-images.githubusercontent.com/62521534/214701056-8c1905b5-73f4-4d20-8125-e8e087234abf.gif)

You can play an online game using the "search" button on the bottom right.
