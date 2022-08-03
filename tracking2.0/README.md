## Tracking2.0

### *YIHENG SU*
### *Summer 2022*

#### I. Description of Tracking2.0
The tracking2.0 project is designed for human and robot interactions with non-linguistic utterance sounds under the supervision of Professor Hannen Wolfe. 

We want to design a user study to test how people perceive emotive sounds from robots. In the study, the participant will give the robot a colored (red, yellow, green, and blue) ball and the robot responds audibly to the given ball. Then, we will ask the participant how the robot feels about the colored ball. We plan to randomize the study so that different colors represent the different emotions of each participant. We also want the sound to be generative so that each sound the participants hear is different.

We need to design motions and a vision processor to set up the robot for the study. In tracking2.0, the robot can track a colored ball and raise its arms after tracking for some time. After the participant put the ball in his hands, the robot can make an emotive sound corresponding to the color of the ball. After the participant removes the ball, the robot will put down his arms and be ready for the next colored ball.

The programs in tracking2.0 are mostly written in C++ and specially designed for the DARwIn-OP robot which is a miniature-humanoid robot platform. The tracking2.0 basically has two parts: main and VisionMode. It also contains a Makefile, which can compile the program in tracking2.0.

#### II. Introduction of Programs

##### 1. main.h and main.cpp
The main.cpp includes all the motions and vision processing in it. It will call the actions, track the colored balls, identify different colors, and play emotive sounds. It can randomly generate a list of emotive sounds so that each sound the participants hear is different.

##### 2. VisionMode.h and VisionMode.cpp
The VisionMode can convert red, yellow, blue, and green into different integers. Red is 1, yellow is 2, blue is 4, and green is 8. It can play different sounds according to different colors.

#### III. Usage of Tracking2.0

##### 1. Run tracking2.0 on the robot
Turn on the robot.
Open the terminal and type:

*sudo su* **(Password is 111111)**

*cd /darwin/Linux/project/tracking2.0*

*killall demo* **(type this if you cannot run the following command)**

*./tracking*

##### 2. Edit tracking2.0 on the robot
Turn on the robot.
Open the terminal and type:

*sudo su* **(Password is 111111)**

*cd /darwin/Linux/project/tracking2.0*

*gedit filename*

*make* ***(after modifying the codes, you need to recompile before running)***

#### IV. Acknowledgement
I would like to thank my summer research Professor Hannen Wolfe. She gave me the opportunity for this research and supported me to design the programs for the robot.

I would also like to thank my research partner Baron Wang, who I worked with during summer of 2022.