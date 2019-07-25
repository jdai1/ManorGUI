# ManorGUI
Creating a GUI via PyQt5 for the backend calls of Swiss department store, Manor.

## Introduction
The purpose of this GUI application is to allow simple and comfortable interactions for the backend function calls of the
Manor store. However, without having access to the Manor backend, a mock_server and one extra parameter are neccesary to
simulate real-time calls to the backend. Four parameters are required as input for the function run:

1. IP Adress  
2. Port
3. Payload
4. Timer

While the IP Adress, Port, and Paylod are neccessary parameters to cary out regular calls to the Manor backend, the Timer
parameter simulates the specific time in which the function is to be completed. In addition, the GUI also comes with an
exportation functionality, allowing the resulting contents of a function call to be exported to a specified file. On a
status tab, a progress bar along with an application log relay information regarding the function calls steps and general
progress.

## Installation

While a stand-alone executable of the ManorGUI could be downloaded from the terminal/command-line with 'pyinstaller --onefile -w ManorRun.py', the maven installation offers a simpler and more effective download. Once the pom.xml, src, and target folders are successfully downloaded, navigate to the folder containing the files. Run 'mvn install' within the Manor-maven folder, generating the contents displayed within the pyinstaller executable. Within the distributable (dist) folder, the application can then be opened.
