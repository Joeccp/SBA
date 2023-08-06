# Cinema house

A cinema 'house' is the basic component of a cinema. 
Each house has a 2-D rectangular seating plan with **1-99 row(s)** and **1-26 column(s)**. 
The seating plan of a house is fixed and cannot be changed later.

Every seat of the seating plan has one of the three following status:
- _Empty_ -- available for sale
- _Sold_ -- occupied and not for sale
- _Reserved_ -- reserved by administrator and not for sale

Each house can have a movie name, which indicates the currently playing movie.

Each house has a unique house number, which is used to identify different houses.


## HOWTO: Create a house
Login as an **administrator**, enter mode `1`(Create house), 
enter the number of rows and columns of the house.
You may choose to enter the movie name, or leave it blank.

Every seat will be set as Empty as default.


## HOWTO: See the seating plan of a house
Login as an **administrator**, enter mode `5`(Check houses information), 
enter the house number.

OR

Login as a **user**, enter mode `1`(Buy ticket), enter the house number. 
User can see seating plan of an available house.
> **Note**
> 'Available house' refers to house that has empty seat(s), 
> and has a movie playing (has movie name).


## HOWTO: Change the movie of a house
Login as an **administrator**, enter mode `2`(Update movie), enter the house number,
enter the *new* movie name, or leave it blank if no movie is playing.

After entering the new movie name, 
you will be asked whether you would like to 'clear all relevant data'.
It means whether you would like to delete all the tickets of the same house, 
and reset all the status of seats of the house to _Empty_.


## HOWTO: Clear all seats of a house
Login as an **administrator**, enter mode `9`(Clear all seats of a house), 
enter the house number.


---

Copyright © 2023 Joe Chau, Licensed under the 
<a href="https://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License, Version 2.0</a>.