## Tracking2.0

### *YIHENG SU*
### *Summer 2022*

#### Description of Tracking2.0
The tracking2.0 project is designed for human and robot interactions with non-linguistic utterance sounds under the supervision of Professor Hannen Wolfe. 

We want to design a user study to test how people perceive emotive sounds by robots. In the study, participant will give robot a colored (red, yellow, green, and blue) ball and the robot responds audibly to the given ball. Then, we will ask the participant how the robot feels about the colored ball. We plan to randomize the study so that different colors represent different emotions fro each participant. We also want the sound to be generative so that each sound the participants hear is different.

Wwe need to design motions and a vision processor to set up the robot for the study. In the tracking2.0, the robot can track a colored ball and raise it arms after tracking for some time. After the participant put the ball in his hands, the robot can make a emotive sounds corresponding to the color of the ball. After the participant removes the ball, the robot will put down his arms and ready for the next colored ball.

The programs in the tracking2.0 is mostly written in C++ and especially designed for the DARwIn-OP robot which is a miniature-humanoid robot platform. The tracking2.0 basically has two parts: main and VisionMode. It also contains a Makefile, which can compile the program in tracking2.0.

#### Introduction of Programs

##### main.h and main.cpp
The main.cpp includes all the motions and vision processing in it. It will call the actions, track the colored balls, identify different colors, and play emotive sounds. It can randomly generate a list of emotive sounds so that each sound the participants hear is different.

##### VisionMode.h and VisionMode.cpp
The VisionMode can convert red, yellow, blue, and green into different integers. Red is 1, yellow is 2, blue is 4, and green is 8. It can olay different sounds according to different colors.

#### Usage of Tracking2.0

##### Run tracking2.0 on the robot
Turn on the robot.
Open the terminal and type:

*sudo su* **(Password is 111111)**

*cd /darwin/Linux/project/tracking2.0*

*killall demo* **(type this if you cannot run the following command)**

*./tracking*

##### Edit tracking2.0 on the robot
Turn on the robot.
Open the terminal and type:

*sudo su* **(Password is 111111)**

*cd /darwin/Linux/project/tracking2.0*

*gedit filename*

*make* ***(after modifying the codes, you need to recompile before running)***

#### Acknowledgement
I would like to thank my summer research Professor Hannen Wolfe, who organized this reasearch and supported me to design the programs for the robot.

I would also like to thank my research partner Baron Wang. We worked together on this research topics this summer.


