# FreeQ

A Python-based program to track queueing in Overwatch using image recognition. Through Discord integration, users can receive notifications when a game is found, eliminating the need to be physically present at the PC.

## Description

This is an old project I created for myself. In high ranks of Overwatch, queues could last up to 30 minutes. Not wanting to wait at the PC for an uncertain amount of time, I'd queue up and leave to do something else. However, being marked as inactive when a game is found results in match cancellation and penalties. So, I developed an application to send a push notification to your phone via a Discord webhook when a game is found. This *frees* users from having to stay at the computer. The application, usable by several users at once within the same server, only pings the user whose queue has popped. It also tracks the time taken to find a game and the selected game mode.
![image](https://github.com/luis-zc/FreeQ/assets/95542273/4c07a43d-b266-43c6-a89d-243827b13482)

## Status

Since I stopped playing Overwatch and the original game was discontinued for the sequel, Overwatch 2 (which also has much shorter queue times :D), this project was never continued. I had planned to release it publicly and add more features but never got around to it. It remains here as a fun endeavor, but I won't be working on it any further. 

## Getting Started

### Dependencies

- Python 3.x
- pyautogui
- discord.py
- dhooks

### Installing

1. Clone the repository:
   ```
   git clone https://github.com/luis-zc/FreeQ.git
   ```
2. Navigate to the project directory:
   ```
   cd FreeQ
   ```
3. Install required packages:
   ```
   pip install pyautogui discord.py dhooks
   ```

### Executing the Program

After installing the required packages, execute the program with:
```
python app.py
```

### Note on Installation

I originally intended to create an installer. Some assets/configs for this are still present in the repository. It worked, but as I was the only user, launching it as a Python script was simpler.  

## Usage

![image](https://github.com/luis-zc/FreeQ/assets/95542273/9f1c62af-49b1-44f3-8a30-4ca1161671ca)


1. Add the Webhook URL and UserID:\
   Online tutorials are available on how to obtain these values. Once you have them, open settings in the top left corner, enter them in their respective fields, and save. A success message should appear. Then, close the window.
2. Start Queue Detection:\
   Enter an Overwatch queue and press Start in the FreeQ program. The program status should switch to "Queue detected". Ensure Overwatch remains unminimized while in the queue. You can leave the PC now.
3. Wait for the Push Notification:\
   FreeQ will send you a Discord notification once a game has been found. Good luck!


## Contact
Luis Zettel Cruz - Luis@zettelcruz.de\
Project Link: [https://github.com/luis-zc/FreeQ](https://github.com/luis-zc/FreeQ)
