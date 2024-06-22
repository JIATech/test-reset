# AutoResetV4

"Project" to write "/reset" or "/mreset" in some Mu Online server because I'm too busy.

## Description

This "project" is about relive some of my childhood while doing other things. I'm too lazy to do it manually, so I decided to write a script to do it for me.

It checks for the window title of the game and if it matches the conditions, it performs the reset or master reset.

Conditions are:

- Level 380 to 400 for a normal reset
- 10 Resets to 50 for a master reset

The script is written in Python and uses the `pydirectinput` library to simulate keyboard input.

Maybe is not the best way to do it, but it works for me. Also it crash sometimes and you have the script to do it's thing when the conditions are met.

## Getting Started

Know some python? Have it installed in your system? No? No problem, I already compiled a Windows executable in the dist folder.