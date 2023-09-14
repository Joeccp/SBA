This folder holds data used in the program.

Houses and tickets data are stored at `data/houses` and `data/tickets` precisely 
(without a filename extension).

> **Technical details**
> 
> `data/houses` and `data/tickets` are binary files, containing 
> <a href="https://docs.python.org/3/library/pickle.html" target="_blank">pickled Python objects</a>.
> Those files are NOT human-readable.

Colour scheme setting is stored at `data/colour.txt`.

Accounts data are stored at `data/accounts.toml`.

See [documentation](../docs/dataStorage.md).
