# Embodied_Project

This is a gamified version of taking user feedback according to visual signals if they helped them throughout the journey. 
The game starts with a character spawning at [0,0] position. The goal is to reach the Green tile(End).There are some tiles that have bombs under them but they are not visible. The player has to navigate through them without dying. Which is almost an impossible task without having some visual queues or signals. 
There are 2 version, 1 with the visual queues and 1 without. 

# With Visual help
The player will be warned if they are in a close proximity of the mines. They can change their path according to reach the final goal. Once they reach the goal a popup asks for feedback about the signals if they helped the player or not.
After that it saves the feedback and the steps took to reach the goal.
Same thing happens in case the player dies.

# Without Visual help
The player is not warned about the positions of the mines and they have no clue about where the next mine could be. It is almost an impossible task to acheive. When the player dies it saves the number of steps player took before they died or if they are lucky enough to reach the goal blindly.

The feedback and steps are stored in CSV files respectively.