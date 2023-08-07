# Ticket

Ticket is generated when a User has bought a seat.

Each ticket indicates the following information about a purchase of a movie ticket.
- Date and time of the purchasing
- House number of the movie
- Movie name
- Seat number (Row number and column number)

**Ticket number starts with a 'T', followed by at least 5 digits.**

## HOWTO: Buy a seat as a user

1. Login as a **user**, enter mode `1`(Buy ticket), enter the house number.
2. You can now see the seating plan of the house. Choose a seat.
3. Enter the row and column number of the seat. 
Whitespaces between row and column number is fine.
Row number is a positive decimal integer starts from 1.
Column number is a single alphabet character.
4. Your purchase is successful, 
and you should see your ticket number and information indicating this purchase.


## HOWTO: Check ticket information
Login as a **user**, enter mode `2`(Check ticket), enter the ticket number.

OR

Login as an **administrator**, enter mode `7`(Check ticket information),
ALL ACTIVE tickets information will be printed.

> **Note**
> 
> 'ACTIVE tickets' refers to tickets that are not refunded by user 
> or deleted by administrator.


## HOWTO: Get refund of a ticket / Delete a ticket
Login as a **user**, enter mode `3`(Ticket refund), enter the ticket number.

OR

Login as an **administrator**, enter mode `8`(Delete ticket), enter the ticket number.

<br/>

They do the *same* thing.


---

Copyright © 2023 Joe Chau, Licensed under the 
<a href="https://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License, Version 2.0</a>.