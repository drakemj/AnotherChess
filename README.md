<h1>Another Chess Project</h1>
  <p>The goal of this project is to create an LED chess board which will light up possible moves you can make, with player vs. player and player vs. AI capability.</p>

<h2>Key Functionality</h2>
  <p>The position of the pieces will be tracked via the enclosed program running in a Raspberry Pi. To index moves a player would like to make, we will first prototype
  a keypad which will take inputs. In the case of an AI, the board will light up to the square that will be played. The board will be made up of 8x8 LED matrix squares,
  each of which will represent 4 4x4 squares that we will use for the board. 16 gpio pins will control these LED squares.

<table><h2>Planned Features</h2><ul>
<li>Stronger AI</li>
<li>Saving your game, so that you can pick it up another time</li>
<li>Cool board animations</li>
<li>Time control + other settings</li>
<li>Other gamemodes, including LED board exclusive modes</li>
<li>Sensors such that a keypad is not needed</li></table>

