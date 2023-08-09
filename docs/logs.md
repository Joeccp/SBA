# Logs in program

Logs are mainly used to trace user/admin input and activities.

Log files are `.txt` files stored in the `logs` directory.

Logs cannot be view and deleted by user/administrator *in the program*. 
(Of course no one can stop you from deleting them manually.)

It is expected that log files can:
1. help **back-end** staff to analyze user/administrator behaviors (for marketing research and other things); and
2. help system maintainer to debug and improve this program (for improving UI/UX for example).

Log files in this program rarely show user inputs directly. 
It is intended to keep our focus of the log file to the two purposes above. 
Plus, recording and tracking every single user input is very creepy.


LOG FILES ARE NOT DATABASE,
THEY SHOULD NOT BE USED TO CHECK OR REVIEW LARGE AMOUNTS OF INFORMATION/DATA
(SUCH AS HOUSES AND TICKETS INFORMATION).


## About the log messages
The name of the log files is the time of executing the program.
The format of a log message is:

```%(asctime)s --> %(levelname)s @%(name)s --> %(message)s```

Where `%(asctime)s` is the time, `%(levelname)s` is the log level, `%(name)s` is where the log 
message was sent, `%(message)s` is the log message. Most of the log information 
should be, and is designed to be, very intuitive and straight forward.

(P.S. In most of the circumstances, `name` is the function / method name where the log
message was sent.)



<br/><br/>

---
<small>
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED",
"MAY", and "OPTIONAL" in this document are to be interpreted as
described in 
<a href="https://www.rfc-editor.org/bcp/bcp14" target="_blank">BCP 14</a>
[<a href="https://www.rfc-editor.org/rfc/rfc2119" target="_blank">RFC2119</a>]
[<a href="https://www.rfc-editor.org/rfc/rfc8174" target="_blank">RFC8174</a>]
when, and only when, they
appear in all capitals, as shown here.
</small>

---

Copyright © 2023 Joe Chau, Licensed under the 
<a href="https://www.apache.org/licenses/LICENSE-2.0" target="_blank">Apache License, Version 2.0</a>.