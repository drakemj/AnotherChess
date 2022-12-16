# Another Chess Project
The goal of this project is to train an AI using a camera to determine the position of a chessboard. With this function comes many different applications such as AI, connectivity with Lichess, move suggestions, etc. Though there is no real reason to reinvent the wheel and rebuild all of the chess functionality that is included in this project (such as legal move checking), it is fun. :)

## Key Functionality
The enclosed program will keep track of the board. The current state of the board as viewed by the AI will be displayed on the board. As a move is made, the screen will indicate the legality of the move. Different gamemodes can be selected via a UI.

## Planned Features
- Saving your game, so that you can pick it up another time
- Time control + other settings
- Connectivity to Lichess

## Installation
While in the root directory, install required libraries by running

`pip install -r requirements.txt`

Then, you can run the application by running

`python3 src/AnotherChess.py`

and if things are successful, you should see the following window.
![image](https://user-images.githubusercontent.com/62521534/208006959-cf0b6e4c-d129-4dcf-afa5-897e9d7df333.png)


