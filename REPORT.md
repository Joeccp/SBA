# SBA Report

## Design

Some tools are used for the software engineering of this project.

### Flowchart
Here is a flowchart showing the basic structure of this program:
![Flow chart showing the basic structure of this program](images/report/Main_Flow_Chart.jpg)

### Pseudocode

After further refinement and improvement, here is the pseudocode of the main program:

```text
The main program (function)

 1 | Initialize the log function
 2 | if the system is not Windows then
 3 |     exit the program
 4 | if the Python version is too old then
 5 |     exit the program
 6 | Clear the screen
 7 | Set the color of the terminal
 8 | Load saved data
 9 | while true do
10 |     input username
11 |     input password
12 |     if the username and password not correct AND it is the admin's account then
13 |         break the loop
14 | adminMode()
15 | while true do
16 |     input username
17 |     if the username exists then
18 |         input password
19 |         if the password is correct then
20 |             if the username is admin then
21 |                 adminMode()
22 |             else
23 |                 userMode()
```

## Implementation

### Features

### Key factors 