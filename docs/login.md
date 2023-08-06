# Login


Login is required to access the system.

To login, enter the username then the password.
Password will not be shown when you are typing.

Due to the fact that this is just an SBA homework, and is in Elective Part D,
hashed usernames and passwords are stored locally in `accounts.toml`, 
instead of using any kind of web-server or database.

You *cannot* add or remove any user, even you are an administrator,
you also *cannot* change the username or password of any user.

**First time logging in will require you to login as an administrator.**

---

Here are all the user accounts:

| Username | Password | Account Type  |
|:--------:|:--------:|:-------------:|
|  admin   |  pass,   | Administrator |
|   user   |  bhjs.   |     User      |

Leading and trailing whitespaces are automatically ignored in the program.

To logout, enter mode `0`(EXIT CONTROL PANEL) if you are in the Control Panel, otherwise,
enter mode `0`(LOG OUT).


---

Copyright © 2023 Joe Chau, Licensed under the 
<a href="https://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License, Version 2.0</a>.