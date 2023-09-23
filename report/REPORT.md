<!-- README
This markdown file is designed to be read online only.
Visit https://joeccp.github.io/SBA/REPORT.html 
-->


<!-- https://mermaid.js.org/config/usage.html#using-mermaid -->
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
</script>


# SBA Report -- by Joe Chau

## Design

Some tools are used for the software engineering of this project.

### Waterfall Model

Waterfall Model is used when developing this project.

<pre class="mermaid">
flowchart LR
    Requirements -->
    Design -->
    Implementation -->
    Testing -->
    dpm[Deployment] -->
    mtn[Maintenance] --> dpm
</pre>

`Requirements`: I studied and analysis the requirements carefully, 
to ensure I have fulfilled and will implement all the required features.

`Design`: In the very beginning, I choose to use the 'menu and mode' design for the user interface 
(which is, providing different menus for administrator and user respectively,
and each menu has different modes).
I decided to encapsulate all the scripts into one single Python package, the basic structure
of the program was designed:
```text
# The structure of my very early prototype of this program

__init__.py
__main__.py
├── admin.py
├── colour.py
├── House.py
├── user.py
├── common.py
├── accounts.toml
```
I hence had a basic concept of the modularity of this program.

`Implementation`: See [Implementation](#implementation)

`Testing`: This program was tested so many times. I simulated all different kinds of 
scenarios, and possible inputs of the users. 
Moreover, there are unittests which test one of the utility programs,
(using the builtin `unittest` module).
You may find the unittest script in the `tests` directory.
(For what it's worth, I also use linter (`flake8` for style checking and `mypy` for type checking) 
to check my code style to ensure a good readability.) 
All the above tests are automated using `GitHub actions` 
with the help of `tox` and `pytest`, 
those tests are automatically done when I `push` my code into the GitHub repository.

`Deployment`: (Skipped as this is just a simulation of the kiosk system)

`Maintenance`: There are bug fixes and updates regularly. 
You may check the [commits history](https://github.com/Joeccp/SBA/commits/main)
and all the [releases](https://github.com/Joeccp/SBA/releases).


### Flowchart
Here is a flowchart showing the basic structure of this program:
![Flow chart of the main program](../images/report/Main_Flow_Chart.jpg)


### Pseudocode

After further refinement and improvement, here is the pseudocode of the main program:

```text
The main program (function)

 1 | Initialize the log function
 2 | if the system is not Windows then
 3 |     exit the program
 4 | if the Python version is too old then
 5 |     exit the program
 6 | Load and initialize the language setting
 7 | Load and initialize the colour scheme
 8 | Clear the screen
 9 | Set the color of the terminal
10 | Load saved data
11 | while true do
12 |     input username
13 |     input password
14 |     if the username and password are correct AND it is the admin's account then
15 |         break the loop
16 | adminMode()
17 | while true do
18 |     input username
19 |     if the username exists then
20 |         input password
21 |         if the password is correct then
22 |             if the username is admin then
23 |                 adminMode()
24 |             else
25 |                 userMode()
```

## Implementation

### Features

Required features:
- [X] [Login system](../docs/login.md)
- [X] [House and movie creation](../docs/house.md)
- [X] [View seating plan](../docs/house.md#howto-see-the-seating-plan-of-a-house)
- [X] [Seat selection](../docs/ticket.md#howto-buy-a-seat-as-a-user)
- [X] [Status storage](../docs/dataStorage.md)
- [X] [Calculation (of the total number of the tickets sold)](../docs/ticket.md#howto-check-ticket-information)

Large additional features:
- [Ticket operation](../docs/ticket.md)
- [Admin seat status override](../docs/seatStatusOverride.md)
- [Supports two langauge](../docs/language.md)
- [Supports two colour scheme](../docs/colour.md)
- [Log files](../docs/logs.md)
- Help function / Documentation


## Related files
- [Problem Analysis](Problem_Analysis.md)
- [Acknowledgement](acknowledgement.md)
- [Self-evaluation](self_evaluation.md)

---

Copyright © 2023 Joe Chau, Licensed under the 
<a href="https://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License, Version 2.0</a>.
