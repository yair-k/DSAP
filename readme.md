
# DTAP - Digital String Art Platform

**Version**: 1.0  
**Author**: Yair K.

## Overview

DTAP (Digital String Art Platform) is an interactive application that lets users create digital string art. It provides a graphical user interface built using `customtkinter` and integrates cloud functionalities like Firebase for storing user data and artworks, along with OpenAI for providing hints and suggestions for the artwork. The platform supports both single-player and multiplayer modes.

## Features

-   **Single Player Mode**: Create string art by yourself.
-   **Multiplayer Mode**: Collaborate with others to create a shared piece of art.
-   **Firebase Integration**: Store and retrieve user profiles and artwork in Firebase.
-   **OpenAI Integration**: Get suggestions for string art using OpenAI's GPT models.
-   **Customizable Settings**: Change nail color, string color, string thickness, and background.
-   **Modern UI**: Built with `customtkinter` for a modern and responsive user experience.

## Project History

DTAP started as a project for the ENGINEERING 1P13A Class at McMaster as the first assignment in Python, and Yair got tired from being tired from studying for midterms so decided to tackle this monstrosity of a project.

## Folder Structure

The following is the typical folder structure of the DTAP project:

```
├── DSAP_master.py           # Main program file (GUI and app logic)
├── DSAP_minified.py         # Minified version of the main program for deployment
├── .env                     # Environment variables for sensitive information (API keys)
├── ________.json  			 # Firebase credentials file
├── icon.ico                 # Icon used for the application
├── icon.png                 # PNG version of the icon
├── requirements.txt         # List of dependencies
```

### Explanation of Main Components

-   **DSAP_master.py**: This is the main file where the core logic of the application resides. It includes the GUI components using `customtkinter`, Firebase integration for data storage, and OpenAI integration for suggestions and hints. The file handles all the game logic, modes (single-player/multiplayer), and user settings.
    
    Key functionalities include:
    
    -   Splash screen with game mode selection.
    -   Customization options for nail color, string color, and string thickness.
    -   Saving and retrieving data from Firebase (credentials are stored in `nails-36418-firebase-adminsdk-cmi75-307c4a5b03.json`).
    -   Utilizing OpenAI API to generate hints for string art.
-   **DSAP_minified.py**: A minimized version of the project, optimized for deployment with fewer comments and shortened code.
    
-   **.env**: This file stores sensitive information like the OpenAI API key and possibly other configuration settings. The key is loaded using the `python-dotenv` package.
    
-   **nails-36418-firebase-adminsdk-cmi75-307c4a5b03.json**: This is the Firebase Admin SDK credentials file. It is necessary for authenticating with Firebase and storing/retrieving user data and art from the Firebase Real-time Database​(nails-36418-firebase-ad…).
    
-   **icon.ico / icon.png**: These are the icons used within the application to provide a visual identity for the platform.
    
-   **requirements.txt**: This file lists the dependencies required to run the project. These include libraries for the GUI (`customtkinter`, `tkinter`, `ttkthemes`), cloud integrations (`firebase-admin`, `openai`), and other utilities (`uuid`, `dotenv`). Full list of dependencies:
    
    
    ```turtle==0.0.1
    Tkinter==0.1.0
    Pillow==10.1.0
    customtkinter==5.1.3
    firebase-admin==6.1.0
    ttkthemes==3.2.2
    webbrowser==1.0
    openai==0.27.8
    python-dotenv==1.0.0
    uuid==1.30``` 
## Installation

### Prerequisites

-   Python 3.7+
-   A Firebase account with a Real-time Database setup.
-   OpenAI API key.

### Setup Instructions

1.  Clone the repository:
   
    `git clone https://github.com/yair-k/DSAP
    cd DSAP` 
    
2.  Install the required dependencies:
   
    `pip install -r requirements.txt` 
    
3.  Set up Firebase:
    
    -   Copy your Firebase Admin SDK JSON credentials to the project root.
    -   Ensure your Firebase Realtime Database is properly set up.
4.  Configure Environment Variables:
    
    -   Create a `.env` file with your OpenAI API key and other sensitive information:
        
        `OPENAI_API_KEY=your_openai_api_key` 
        

## Usage

To run the application, simply execute the main script:

`python DSAP_master.py` 

### Customization Options

-   **Nail Settings**:
    
    -   Nail color can be selected from a variety of options.
    -   Adjust the nail size for different types of string art.
-   **String Settings**:
    
    -   Select string color and string thickness for customization.
    -   Adjust string size dynamically during the game.
-   **Background Settings**:
    
    -   Change the background to different colors for a personalized experience.

### Firebase Integration

-   **User Profiles**: User data, including profile information, is stored in Firebase.
-   **Artworks**: Save your string art to the Firebase Real-time Database, allowing you to access and modify your artwork later.

### OpenAI Integration

-   **Hints and Suggestions**: The game integrates with OpenAI to offer creative suggestions on string patterns based on user input.
