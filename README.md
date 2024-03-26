# trail_cam_IoT
Final Project for IoT. Trail camera using raspberry pi. This project also included a base station that could grab the data from the raspberry pi using node-scp.

## description
* temperature sensor: temp 102
* passive infrared motion sensor
* rasberry pi v2 camera module
* The main goal was to make a system that took pictures when it detected motion with the motion sensor. The temperature sensors' job is to make sure that the important pieces do not turn on or attempt to work when it is too cold for them to function properly. We determined the temperature ranges for the different components using data sheets for each piece.
* The system also has a notification system for when the states change due to the temperature.
* images were given timestamps and the temperature as a text caption in the top left corner of the pictures
* To extract both the images and log file we built a script using node.js that downloads all the files from a specified directory on the raspberry Pi to a specified directory on the local device. The directory on the raspberry pi is then cleared to make room for more photos. Then we built a basic web app to display the images andthe log file. All the logs are stored in a SQL database. 

## Files
* cs380_finalProject.py : the python script that is run with a cron job when the raspberry pi gains power. Handles collecting data from the sensors: temperature and motion. Add captions and titles to the pictures from the camera that include the time and temperature of the device. Shuts down program if it is too cold to function properly.
* cs380Final_Jordan_Cumro.pdf : goes through the sensors, finite state machine, and the setup of the raspberry pi as well as the base station that views the photos.
* cs380_README_CumroJordan.pdf : Reviews the libraries and the versions of software used when building this project. Details the environment setup and how to test the system if needed.
* TrailCameraWebApp : contains the files to run the base station. These files pull and display the images from the rasberry pi.

  ## current limitations
  * uses dateTime to get the time: over time this may drift. With more time we would add a realtime clock to this system.
  * node js was written very system dependent
  * the database hosting the images is missing some pieces we would want to add in the longterm.(deleting images you dont want taking up space)

  ## future additions
  * more environemental sensors: humidity and the amount of light detected could help the system take more reliable pictures and turn off when the pictures may be blurry or dark
  * real time clock
  * machine learning algorithm to try and eliminate pictures taken without an animal or person pictured.

