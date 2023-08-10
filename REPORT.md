<!-- README
This markdown file is designed to be read online only.
Visit https://joeccp.github.io/SBA/REPORT.html 
-->

<!-- https://mermaid.js.org/config/usage.html#using-mermaid -->
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
</script>


# SBA Report -- by Joe Chau

## Design

Some tools are used for the software engineering of this project.

### Waterfall Model

Waterfall Model is used when developing this project.

<pre class="mermaid">
flowchart LR
    Requirements -->
    Design -->
    Implementation -->
    testing -->
    Integration -->
    Maintenance
</pre>


### Flowchart
Here is a flowchart showing the basic structure of this program:
<pre class="mermaid">
flowchart TD
    start([Start])
    ipt1[/Input Admin username and password/]
    check1{Amin's username and password input correct?}
    admin1[["Admin mode
    Control Panel"]]
    ipt2[/Input username and password/]
    check2{Account exists and the corresponding password is correct?}
    check3{Login as?}
    admin2[["Admin mode
    Control Panel"]]
    user[[User mode]]

    start --> ipt1
    ipt1 --> check1
    check1 -- Yes --> admin1
    check1 -- No --> ipt1
    admin1 --> ipt2
    ipt2 --> check2
    check2 -- Yes --> check3
    check2 -- No --> ipt2
    check3 -- Admin --> admin2
    check3 -- User --> user
    admin2 --> ipt2
    user --> ipt2
</pre>

Due to the technical nature of a [mermaid graph](https://mermaid.js.org/),
the flowchart above is indeed a bit messy, 
you may want to see the
[photo version](images/report/Main_Flow_Chart.jpg)
which has a better quality.

### Pseudocode

After further refinement and improvement, here is the pseudocode of the main program:

```text
The main program (function)

 1 | Initialize the log function
 2 | if the system is not Windows then
 3 |     exit the program
 4 | if the Python version is too old then
 5 |     exit the program
 6 | Clear the screen
 7 | Set the color of the terminal
 8 | Load saved data
 9 | while true do
10 |     input username
11 |     input password
12 |     if the username and password not correct AND it is the admin's account then
13 |         break the loop
14 | adminMode()
15 | while true do
16 |     input username
17 |     if the username exists then
18 |         input password
19 |         if the password is correct then
20 |             if the username is admin then
21 |                 adminMode()
22 |             else
23 |                 userMode()
```

## Implementation

### Features

### Key factors 

