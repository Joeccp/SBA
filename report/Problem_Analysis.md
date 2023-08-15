# Problem Analysis
<!-- By Joe Chau. 100% original, no ChatGPT, no AI :)  -->


## Background

Nowadays, the movie industry is rising, with more and more viewers and larger cinema.
More staffs are required to handle more customers.
There is often shortagfe of manpower which leads to a low efficency of ticket selling. 
It is difficult to find suitable employees, and it involves cost of recruiting, human resource management, training, and most importantly, wage.
Also, in order to see what movies are available, customers need to queue up and ask the staff one by one.
It is also very difficult for customers to know which seats are available. They have to ask one by one, which leads to a extremely poor efficency.
A long waiting time causes fewer customers willing to queue and purchase tickets.

Cost of production is high, efficency is low. A more powerful solution is required.
Hence, this move kiosk system is born.


## Solution

## Advantages

We need a strong and stable automated cinema kiosk system. Run by full-auto, can handle many tasks.
This system should be able to let customers to see list of available movie easily,
customers should also be able to see the seating plan and purchase ticket.
Moreover, customers should be able to check the information about their purchased tickets, and be able to get refund.

This system should also porvides a admin control panel, which allows admin to create and modify cinema houses and do seat operation.
This system can be login as user and admin.

### Inplementation analysis

In teerms of software engineering, the software needs:
- A login system, using a local `toml` file. Passwords should be hashed.
- A `House` class, which represents a cinema house, and has the following attributes and methods:
  - `n_row`, `n_column`, `n_seat`, `house_number`: `int`, represenging number of rows and columns, number of seats, and the house number respectivly.
  - `seating_plan`: `list[list[int]]`, a 2D list which store all status of the seat,
    - `0` = Empty, `1` = Sold, `2` = Reserved.
  - `movie`: `str`, the movie name of the currently playing movie
  - `n_available`: `int`, number of available seat.
  - `printPlan(self)`: A function that pretty print the seating plan.
  - `clearPlan(self)`: Clear the seating plan.
  - `n_tickets`: Class method, returns the number of tickets sold in all houses
  - `searchTicket(cls, target_ticket_index: int)`: Searches the ticket with the given ticket index
    - 'ticket index' is a specila format of a ticket number

