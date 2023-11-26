# Self-evaluation

There are many things that I think I can improve when doing this project:

- Ticket data and methods should not be inside the `House` class.
  - Maybe a `Ticket` class?

- My solution of supporting two languages is horrible.
  - Maybe using the builtin `gettext` module?

- Many functions for supporting the colour scheme setting and language setting are overlapped.
  - Maybe group these settings into a single Admin Mode?
  - Maybe store these setting into a single file?

- Admin can't add a custom ticket.
  - Maybe adding a new Admin Mode. After creating the ticket, sort all the tickets inside `House.tickets_table`.

- User can't set the language and colour scheme.
  - Maybe adding a new user mode option
  - Separate Admin's and User's settings (into two different files or folders)?

- User can only buy tickets of movies that are currently playing.
  - Maybe a `Movie` class for each movie in house.
  - Each `House` instance has a movie list, storing the currently playing movie and the movies that will be played.
  - Maybe many same movie playing can be grouped into a single `Movie` instance.
  - Then we will need a largely modified user menu, the logic of buying movie tickets would be changed as follow:
    1. User select the movie.
    2. User select a available date and time of the selected movie.
    3. User select a seat / seats.

---

Copyright © 2023 Joe Chau, Licensed under the 
<a href="https://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License, Version 2.0</a>.
