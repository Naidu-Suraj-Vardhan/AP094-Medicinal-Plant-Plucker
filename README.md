# AP094-Medicinal-Plant-Plucker

![WhatsApp Image 2022-04-03 at 11 36 30 PM](https://user-images.githubusercontent.com/68743810/164063007-8bb2796b-4105-4691-b844-afc014c8c079.jpeg)

### Team Members:
1. Sri Lakshmi Lingineni
2. Abhijeet Medicharla
3. Sushanth Prasad Tallluri
4. [Suraj Vardhan Naidu](linkedin.com/in/suraj-vardhan-naidu-638b911a0)


## Overview:
This project is done under [InnovateFPGA](https://www.innovatefpga.com/portal/) competition 2021-22. This project concentrates on identifying and detecting medicinal plants, plucks them and stores them so that we can replant them thereafter. The following is the block diagram of the architecture of the project:

![BLOCK_DIAGRAM](https://user-images.githubusercontent.com/68743810/164062826-10d37355-3c16-40f1-8921-3edf3f46d79a.png)

Click [here](https://www.youtube.com/watch?v=_inWtxc4onA) to watch Demo Video.

Click [here](https://www.innovatefpga.com/cgi-bin/innovate/teams.pl?Id=AP094&All=1) to view the project.


### Downloading Git:
Download this repo in a zip file by clicking this [link](https://github.com/Naidu-Suraj-Vardhan/AP094-Medicinal-Plant-Plucker/archive/refs/heads/main.zip) or execute this from the terminal: ```https://github.com/Naidu-Suraj-Vardhan/AP094-Medicinal-Plant-Plucker.git ```.


### About Files:
```de10nano(hps).py``` : This file contains python code to be run on ``DE10 Nano`` for plant detection and autonomous movement of the bot and sending the image to cloud and recieving outputs from there.

```haar-cascade-plant-detection.xml```: The trained model saved into xml file through haar cascade algorithm for plant detection.

```medicinal plant detection on cloud``` : This folder contains the files that are deployed on ``Azure Cloud``.

```armcontrol.ino```: This file contains the Arduino code for the movement of the arm which gets it commnands whether to move or not from DE10 Nano.

```downloadFiles.py```: This file contains python code to downloads the predicted predicinal plant images from Cloud.
