# Self-evaluation

There are many things that I think I can improve when doing this project:

- Ticket data and methods should not be inside the `House` class.
  - Maybe a `Ticket` class?

- My solution of supporting two languages is horrible.
  - Maybe using the builtin `gettext` module?

- Many functions for supporting the colour scheme setting and language setting are overlapped.
  - Maybe group these settings into a single Admin Mode?
  - Maybe store these setting into a single file?

- User can't buy more than one ticket at once, even I have finished `SBA.coorutils.coorExprAnalysis()`.
and `SBA.coorutils.getCoorsFromCoorExpr()`.
  - Use them.
  - Change the code logic, so that one ticket does not equal to one seat.

- Admin can't add a custom ticket.
  - Maybe adding a new Admin Mode. After creating the ticket, sort all the tickets inside `House.tickets_table`.

- User can't set the language and colour scheme.
  - Maybe adding a new user mode option
  - Separate Admin's and User's settings (into two different files or folders)?

---

Copyright © 2023 Joe Chau, Licensed under the 
<a href="https://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License, Version 2.0</a>.
