# Data storage

Data is automatically saved.

***Each time saving data will cover the previous saved data.***

Houses and tickets data are stored at `SBA/data/houses` and `SBA/data/tickets` 
(without a filename extension), the colour scheme setting is stored at `SBA/data/colour.txt`,
the language option is stored at `SBA/data/language.txt`
if there are no such files, the program will create them if needed.

When the program is started, it will try to load data.

See documentation on how to change the [colour scheme](colour.md) and [language](language.md).

---

> **Technical details**
> 
> `SBA/data/houses` and `SBA/data/tickets` are binary files, containing 
> <a href="https://docs.python.org/3/library/pickle.html" target="_blank">pickled Python objects</a>.
> Those files are NOT human-readable.


## HOWTO: Manually save and load data
Login as an **administrator**, enter mode `3`(Save Data) to save data or 
mode `4`(Load Data) to load data.


## HOWTO: Delete all data
<!--This is GitHub's warning format-->
> **Warning**
> 
> The following instructions will reset ***everything*** of this program.

Login as an **administrator**, enter mode `11`(CLEAR ALL DATA).
It will clear ALL data: every house, every ticket. 
Saved data will also be deleted.
Colour scheme will be reset to `DARK`.
Language will be reset to `ENGLISH`.
It should reset everything.


---

Copyright © 2023 Joe Chau, Licensed under the 
<a href="https://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License, Version 2.0</a>.
