/*
 * main.cpp
 *
 *  Created on: 2022 6 28
 *      Author: Yiheng Su
 */

// import needed packages and files 
#include <stdio.h>
#include <unistd.h>
#include <limits.h>
#include <string.h>
#include <libgen.h>
#include <signal.h>

#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
#include <ctime>
using namespace std;

#include "mjpg_streamer.h"
#include "LinuxDARwIn.h"

#include "StatusCheck.h"
#include "VisionMode.h"

#ifdef MX28_1024
#define MOTION_FILE_PATH    "../../../Data/motion_1024.bin"
#else
#define MOTION_FILE_PATH    "../../../Data/motion_4096.bin"
#endif

#define INI_FILE_PATH       "../../../Data/config.ini"
#define SCRIPT_FILE_PATH    "script.asc"

#define U2D_DEV_NAME0       "/dev/ttyUSB0"
#define U2D_DEV_NAME1       "/dev/ttyUSB1"

// Set up the robot. DO NOT CHANGE ANY CODE BEFORE THE MAIN FUNCITON
LinuxCM730 linux_cm730(U2D_DEV_NAME0);
CM730 cm730(&linux_cm730);

void change_current_dir()
{
    char exepath[1024] = {0};
    if(readlink("/proc/self/exe", exepath, sizeof(exepath)) != -1)
    {
        if(chdir(dirname(exepath)))
            fprintf(stderr, "chdir error!! \n");
    }
}

void sighandler(int sig)
{
    exit(0);
}

// myrandom function is used in the late std:random_shuffle function
int myrandom (int i) {return std::rand()%i;}

// main function
int main(void)
{
    signal(SIGABRT, &sighandler);
    signal(SIGTERM, &sighandler);
    signal(SIGQUIT, &sighandler);
    signal(SIGINT, &sighandler);

    change_current_dir();

    // Set up and initialize the camera
    minIni* ini = new minIni(INI_FILE_PATH);
    Image* rgb_output = new Image(Camera::WIDTH, Camera::HEIGHT, Image::RGB_PIXEL_SIZE);

    LinuxCamera::GetInstance()->Initialize(0);
    LinuxCamera::GetInstance()->SetCameraSettings(CameraSettings());    // set default
    LinuxCamera::GetInstance()->LoadINISettings(ini);                   // load from ini

    // Create a streamer object
    mjpg_streamer* streamer = new mjpg_streamer(Camera::WIDTH, Camera::HEIGHT);

    // Create a ball tracker and a ball follower object
    BallTracker tracker = BallTracker();
    BallFollower follower = BallFollower();

    // Create red, yellow, green, and blue ball finders and give each finder some parameters
    // The current parameters are adjusted for the lab in Runnals
    // ColorFinder( int hue, int hue_tolerence, int min_saturation, int min_vallue, double min_per, double max_per )
    ColorFinder* red_finder = new ColorFinder(0, 6, 45, 0, 0.3, 50.0);
    red_finder->LoadINISettings(ini, "RED");
    httpd::red_finder = red_finder;

    ColorFinder* yellow_finder = new ColorFinder(60, 15, 45, 0, 0.3, 50.0);
    yellow_finder->LoadINISettings(ini, "YELLOW");
    httpd::yellow_finder = yellow_finder;

    ColorFinder* blue_finder = new ColorFinder(225, 15, 45, 0, 0.3, 50.0);
    blue_finder->LoadINISettings(ini, "BLUE");
    httpd::blue_finder = blue_finder;

    ColorFinder* green_finder = new ColorFinder(120, 35, 45, 0, 0.3, 50.0);
    green_finder->LoadINISettings(ini, "GREEN");
    httpd::green_finder = green_finder;

    httpd::ini = ini;

    //////////////////// Framework Initialize ////////////////////////////
    if(MotionManager::GetInstance()->Initialize(&cm730) == false)
    {
        linux_cm730.SetPortName(U2D_DEV_NAME1);
        if(MotionManager::GetInstance()->Initialize(&cm730) == false)
        {
            printf("Fail to initialize Motion Manager!\n");
            return 0;
        }
    }

    // Initialize the Walking
    Walking::GetInstance()->LoadINISettings(ini);

    // Initialize the Action and Head motors
    MotionManager::GetInstance()->AddModule((MotionModule*)Action::GetInstance());
    MotionManager::GetInstance()->AddModule((MotionModule*)Head::GetInstance());
    // MotionManager::GetInstance()->AddModule((MotionModule*)Walking::GetInstance());

    LinuxMotionTimer *motion_timer = new LinuxMotionTimer(MotionManager::GetInstance());
    motion_timer->Start();
    /////////////////////////////////////////////////////////////////////
    // Set up the robot. DO NOT CHANGE ANY FOLLOWING CODES BEFORE LINE 162
    MotionManager::GetInstance()->LoadINISettings(ini);

    int firm_ver = 0;
    if(cm730.ReadByte(JointData::ID_HEAD_PAN, MX28::P_VERSION, &firm_ver, 0)  != CM730::SUCCESS)
    {
        fprintf(stderr, "Can't read firmware version from Dynamixel ID %d!! \n\n", JointData::ID_HEAD_PAN);
        exit(0);
    }

    if(0 < firm_ver && firm_ver < 27)
    {
#ifdef MX28_1024
        Action::GetInstance()->LoadFile(MOTION_FILE_PATH);
#else
        fprintf(stderr, "MX-28's firmware is not support 4096 resolution!! \n");
        fprintf(stderr, "Upgrade MX-28's firmware to version 27(0x1B) or higher.\n\n");
        exit(0);
#endif
    }
    else if(27 <= firm_ver)
    {
#ifdef MX28_1024
        fprintf(stderr, "MX-28's firmware is not support 1024 resolution!! \n");
        fprintf(stderr, "Remove '#define MX28_1024' from 'MX28.h' file and rebuild.\n\n");
        exit(0);
#else
        Action::GetInstance()->LoadFile((char*)MOTION_FILE_PATH);
#endif
    }
    else
        exit(0);

    // Enable the robot's body to move
    Action::GetInstance()->m_Joint.SetEnableBody(true, true);
    MotionManager::GetInstance()->SetEnable(true);

    cm730.WriteByte(CM730::P_LED_PANNEL, 0x01|0x02|0x04, NULL);

    // Reset status: ask the robot to sit down and stand up
    LinuxActionScript::PlayMP3("../../../Data/mp3/Vision processing mode.mp3");
    Action::GetInstance()->Start(50); // sit down
    while(Action::GetInstance()->IsRunning()) usleep(8*1000);
    Action::GetInstance()->Start(1); // stand up
    while(Action::GetInstance()->IsRunning()) usleep(8*1000);

    Head::GetInstance()->m_Joint.SetEnableHeadOnly(true, true);
    Head::GetInstance()->m_Joint.SetPGain(JointData::ID_HEAD_PAN, 8);
    Head::GetInstance()->m_Joint.SetPGain(JointData::ID_HEAD_TILT, 8);

    // Record how many pixels are in each color
    int color_counters[4] = {0,0,0,0}; //{ red, yellow, blue, green }

    // list of music names
    std::vector<char*> names;
    names.push_back("mp3/happy.mp3");
    names.push_back("mp3/sad.mp3");
    names.push_back("mp3/angry.mp3");
    names.push_back("mp3/content.mp3");

    // Random shuffle the list so that each time each color has a random music.
    std::srand(unsigned(std::time(0)));
    std::random_shuffle(&names[0], &names[4], myrandom);
    // Print out which type of music each color has in the terminal
    cout << "\nRED: " << names[0] << ";\nYELLOW: " << names[1] << ";\nBLUE: " << names[2] << ";\nGREEN: " << names[3] << "\n\n";

    // record the robot has tracked for how long
    int counter = 0;

    // boolean: if robot hold the ball
    int if_hold = 0;

   // boolean: if robot is making sounds
   int ready_to_play = 0;

    printf("Press the ENTER key to begin!\n");
    getchar();

    // The following code run the motions designed for the user study
    // The robot tracks the dominant color in the current screen
    // The robot raises its arms after tracking a ball for some time
    // The robot can hold the ball and make a sound
    // When the participant removes the ball, the robot will put down its arms
    while(1)
    {   
        // Set up ball postion objects
        Point2D ball_pos, red_pos, yellow_pos, blue_pos, green_pos;

        LinuxCamera::GetInstance()->CaptureFrame();
        memcpy(rgb_output->m_ImageData, LinuxCamera::GetInstance()->fbuffer->m_RGBFrame->m_ImageData, LinuxCamera::GetInstance()->fbuffer->m_RGBFrame->m_ImageSize);

        red_pos = red_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);
        yellow_pos = yellow_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);
        blue_pos = blue_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);
	    green_pos = green_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame);

        // The following for-loop goes through all the pixels in the current screen
        // It will identify the four colors and count how many pixels are in each color
        unsigned char r, g, b;
        for(int i = 0; i < rgb_output->m_NumberOfPixels; i++)
        {
            r = 0; g = 0; b = 0;

            if(red_finder->m_result->m_ImageData[i] == 1)
            {
                color_counters[0] ++;
                r = 255;
                g = 0;
                b = 0;
                
            }
            if(yellow_finder->m_result->m_ImageData[i] == 1)
            {
                color_counters[1] ++;
                r = 255;
                g = 255;
                b = 0;
            }
            if(blue_finder->m_result->m_ImageData[i] == 1)
            {
                color_counters[2] ++;
                r = 0;
                g = 0;
                b = 255;  
                    }
            if(green_finder->m_result->m_ImageData[i] == 1)
            {
                color_counters[3] ++;
                r = 0;
                g = 255;
                b = 0; 
            }

            if(r > 0 || g > 0 || b > 0)
            {
                rgb_output->m_ImageData[i * rgb_output->m_PixelSize + 0] = r;
                rgb_output->m_ImageData[i * rgb_output->m_PixelSize + 1] = g;
                rgb_output->m_ImageData[i * rgb_output->m_PixelSize + 2] = b;
            }
        } 

        // Send the current rgb_output to the streamer.
        streamer->send_image(rgb_output);

	    // cout << "red: " << color_counters[0] << "; yellow: " << color_counters[1] << "; blue: " << color_counters[2] << "; green: " << color_counters[3] << "\n";

	    Point2D pos;
        LinuxCamera::GetInstance()->CaptureFrame();

        // Find dominant color in the current screen
        int max_number = color_counters[0];
        int index = 0;
        for (int i = 1; i < 4; i ++) {
            if (color_counters[i] > max_number) {
                max_number = color_counters[i];
                index = i;
            }
        }
	    // cout << "max_num: " << max_number << "; index: " << index << "\n";
	
        // determine which color is dominant in the current screen and track that color
        if (Action::GetInstance()->IsRunning() == 0) 
        {
            if (index == 0) {
                tracker.Process(red_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame));
            }
            else if (index == 1) {
                tracker.Process(yellow_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame));
            }
            else if(index == 2) {
                tracker.Process(blue_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame));
            }
            else if(index == 3) {
                tracker.Process(green_finder->GetPosition(LinuxCamera::GetInstance()->fbuffer->m_HSVFrame));
            }
                    rgb_output = LinuxCamera::GetInstance()->fbuffer->m_RGBFrame;
        }

	    // determine which color the robot sees, convert the color into integer, and pass the integer to the VisionMode class
        int detected_color = 0;
        if (index == 0) {
            detected_color |= (red_pos.X == -1)? 0 : VisionMode::RED; }
        else if (index == 1) {
                detected_color |= (yellow_pos.X == -1)? 0 : VisionMode::YELLOW; }
        else if (index == 2) {
                detected_color |= (blue_pos.X == -1)? 0 : VisionMode::BLUE; }
        else if (index == 3) {
            detected_color |= (green_pos.X == -1)? 0 : VisionMode::GREEN; }

        // record how long has the robot tracking the ball
        if (detected_color != 0)
        {
            counter ++;
        }
        else 
        {
            counter = 0;
        }

        if (counter == 0 and detected_color == 0 and Action::GetInstance()->IsRunning() == 0 and if_hold == 1) {
            LinuxActionScript::PlayMP3("mp3/neutral_descending.mp3");
            Action::GetInstance()->Start(51);
        }

        if (counter == 0 and detected_color == 0 and Action::GetInstance()->IsRunning() == 1 and if_hold == 1) {
            if_hold = 0;
        }


        // When playing the action, reset the counter
        if (Action::GetInstance()->IsRunning() == 1) 
        {
            counter = 0;
            
        }

        // Reset the counter when it is greater than 30
        if (counter > 30)
        {	
            ready_to_play = 0;
        }

        // Raise robot's arms after tracking the ball for some time
        if (counter > 10 and if_hold == 0 and Action::GetInstance()->IsRunning() == 0) 
        {	
            LinuxActionScript::PlayMP3("mp3/neutral_ascending.mp3");
            Action::GetInstance()->Start(48);
            if_hold = 1;
            ready_to_play = 1;
        }

        // when counter is greater than 20, play the motion
            if (counter > 10 and if_hold == 1 and ready_to_play == 1 and Action::GetInstance()->IsRunning() == 0) 
        {
                VisionMode::Play(detected_color, names);
        }

        cout << "Color dectected: " << detected_color << " ;Counter: " << counter << "; Action: " << Action::GetInstance()->IsRunning() << "; hold: " << if_hold << "; ready: " << ready_to_play << "\n";
        // reset color counters
        color_counters[0] = 0;
        color_counters[1] = 0;
        color_counters[2] = 0;
        color_counters[3] = 0;
    }

    return 0;
}
