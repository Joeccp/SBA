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

---

Copyright © 2023 Joe Chau, Licensed under the 
<a href="https://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License, Version 2.0</a>.
