# Data storage

Data is automatically saved.

**Each time saving data will cover the previous saved data.**

Data are stored at `SBA/data/houses` and `SBA/data/tickets` (without a filename extension), 
if there are no such files, the program will create them.

When the program is started, it will try to load data.

---
> Technical details:
> 
> Those files are binary files, containing [pickled Python objects](https://docs.python.org/3/library/pickle.html).
> Those files are NOT human-readable.


## HOWTO: Manually save and load data
Login as an **administrator**, enter mode `3`(Save Data) to save data or `4`(Load Data) to load data.


## HOWTO: Reset everything
<!--This is GitHub's warning format-->
> **Warning**
> The following instructions will reset ***everything*** of this program.

Login as an **administrator**, enter mode `10`(CLEAR ALL SAVED DATA).
It will clear ALL saved data: every house, every ticket. 
Saved data will also be deleted.


---

Copyright © 2023 Joe Chau, Licensed under the 
<a href="https://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License, Version 2.0</a>.