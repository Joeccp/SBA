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

`Deployment`: (Skipped as this is just a simulation of the kiosk system)

`Maintenance`: There are bug fixes and updates regularly.


### Flowchart
Here is a flowchart showing the basic structure of this program:
![Flow chart of the main program](images/report/Main_Flow_Chart.jpg)


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

Required features:
- [X] [Login system](docs/login.md)
- [X] [House and movie creation](docs/house.md)
- [X] [View seating plan](docs/house.md#howto-see-the-seating-plan-of-a-house)
- [X] [Seat selection](docs/ticket.md#howto-buy-a-seat-as-a-user)
- [X] [Status storage](docs/dataStorage.md)
- [X] [Calculation (of the total number of the tickets sold)](docs/ticket.md#howto-check-ticket-information)

Large additional features:
- [Ticket operation](docs/ticket.md)
- [Admin seat status override](docs/adminSeatOperation.md)
- Help function / [Documentation](README.md)


### Key factors 

#### Data Structure
> **Note**
> 
> Unless other specified, in the following section, all the data structure I talk about
> is a Python object type.

- Class is used as the type of cinema house. Every house is a `House` instance.
- Dictionary is used as a register table of all the houses.
- Functions are used literally everywhere in this program one example is the `main()` function.
- Data is stored as two pickle files, which are binary files. 
They were opened with `open()`, which returns a file object.
- Two-dimensional list is used two store tickets information.
- And more

#### Variable declaration and initialization
Most of the variables in the program have a straight forward name.

> **Note**
> 
> The coding style I use is based on 
> <a href='https://peps.python.org/pep-0008' target='_blank'>PEP 8</a>.

Naming convention I use:
- Normal variables use `lower_case_with_underscores`
- Special variables and constants use `UPPER_CASE_WITH_UNDERSCORES`
- Functions use `mixedCase`
- Module name use `lowercase`, such as `utils.py`

When I declare or assign variable, function or method, 
I use type hints to clarify its type, argument or return value.

Python does not require initialization before assigning a variable.


#### Data collection, Input and Validation




#### Data Processing


#### Program Output


#### Interface of the Program


#### Modularity


#### Reusability


#### Portability


#### System development cycle


#### Sorting and searching algorithms
This program uses Linear Search when searching specific ticket.

> **Note**
> 
> As the tickets are created with a unique ticket number assigned with ascending order
> and stored at the ticket list, tickets are already sorted with ascending order.

```text
Pseudocode of using Linear Search to search ticket

 1 | ticket = []
 2 | for i from 0 to len(ticket_list) - 1 do
 3 |     if ticket_list[i, 0] = the target ticket number
 4 |         ticket ← ticket_list[i]
```


---
By Joe Chau