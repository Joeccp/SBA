# Problem Analysis
<!-- By Joe Chau. 100% original, no ChatGPT, no AI :)  -->


## Background

Nowadays, the movie industry is rising, with more and more viewers and larger cinema.
More staffs are required to handle more customers.
There is often a shortage of manpower which leads to a low efficiency of ticket selling. 
It is difficult to find suitable employees, and it involves cost of recruiting, human resource management, training, and most importantly, wage.
Also, in order to see what movies are available, customers need to queue up and ask the staff one by one.
It is also very difficult for customers to know which seats are available. They have to ask one by one, which leads to a extremely poor efficency.
A long waiting time causes fewer customers willing to queue and purchase tickets.

The Cost of production is high, efficiency is low. 
A more powerful solution is required.
Hence, this move kiosk system is born.


## Solution

## Advantages

We need a strong and stable automated cinema kiosk system,
run by full-auto, and can handle many tasks.
This system should be able to let customers see a list of available movies easily,
customers should also be able to see the seating plan and purchase ticket.
Moreover, customers should be able to check the information about their purchased tickets, and be able to get refund.

This system should also provide an admin control panel, 
which allows admin to create and modify cinema houses and do seat operation.
This system can be login as user and admin.

### Implementation analysis

In terms of software engineering, the software needs:
- A login system, using a local `toml` file. Passwords should be hashed.
- A `House` class, which represents a cinema house, and has the following attributes and methods:
  - `n_row`, `n_column`, `n_seat`, `house_number`: `int`, representing number of rows and columns, number of seats, and the house number respectivly.
  - `seating_plan`: `list[list[int]]`, a 2D list which stores all status of the seat,
    - `0` = Empty, `1` = Sold, `2` = Reserved.
  - `movie`: `str`, the movie name of the currently playing movie
  - `n_available`: `int`, number of available seats.
  - `printPlan(self)`: A function that pretty prints the seating plan.
  - `clearPlan(self)`: A function that clears the seating plan.
  - `adult_price`: `int`, movie ticket price for adults.
  - `child_price`: `int`, movie ticket price for children.
  - `house_revenue`: `int`, the house revenue.
  - `n_tickets`: A class method, returns the number of tickets sold in all houses
  - `searchTicket(cls, target_ticket_index: int)`: A class method. It searches the ticket with the given ticket index
    - 'ticket index' is a special format of a ticket number
  - `total_tickets`: `int`, a class attribute that stores the total number of tickets sold, including those refunded tickets.
  - `total_revenue`: `int`, a class attribute that stores the total revenue of all houses.
- Data save and load function, which uses local `pickle` Python file.
  - `saveData()` and `loadData()`, functions that save and load local data.
- `adminMode()` and `userMode()`, functions which encapsulate the admin mode and user mode.

This system targets Windows 10/11, Python 3.11+.


---

Copyright © 2023 Joe Chau, Licensed under the 
<a href="https://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License, Version 2.0</a>.
