# **termicol**
A [**python**](https://www.python.org) Simple **python** function aimed to handle printing of colored and / or decorated text to console / terminal.
<br />
<br />
​<br />
## Installation
With `git` [GitHub](https://github.com/irtsa-dev/termicol):
```
git clone https://github.com/irtsa-dev/termicol.git
```
With `pip` [PyPi](https://pypi.org/project/idev-termicol/)
```
pip install idev-termicol
```
<br />
<br />
<br />
<br />
<br />
<br />

## Usage
To import:
```py
from termicol.termicol import *
```
<br />

Then, later on you may utilize:
```py
tprint(content: str, end: str = '\n')
# Prints off text and background in the given color with provided decorations.
# To do so, <> is used similar to html.
# Example being: <t=white>hello

showColorList()
# Prints off a list of valid arguments for color.

showDecorationList()
# Prints off a list of valid arguments for decoration.
```
​
<br />
<br />
### Code Examples
```py
from termicol.termicol import tprint

tprint("<t=red>hello, this text will be red!")
```
```py
from termicol.termicol import *

tprint("<t=blue>this text will be blue,<t=red> While this text will be red!")
```
```py
from termicol.termicol import *

tprint("<t=red><b=blue><d=underline>This will be underlined red text with blue background!")
```
```py
from termicol.termicol import *

tprint("<t=red><b=blue>This will be red text with a blue background!<r>This will now be the default text.<t=red> Back to red text!<b=white> A blue backround is added.<r=b> Background is now default.")
```
​
<br />
<br />
### Additional Notes
Valid tags to utilize:
- t | textcolor
  - Will change the text color, can either be one of the valid color arguments that are seen in `showColorList()` function or a list of 3 values separated by a comma for rgb values.
  - \<t=red\> | \<t=20,2,30\>
- b | bgcolor | backgroundcolor
  - Will change the background color, can either be one of the valid color arguments that are seen in `showColorList()` function or a list of 3 values separated by a comma for rgb values.
  - \<b=red\> | \<b=20,2,30\>
- d | deco | decorations
  - Will add in decorations based on what is provided, must be ones provided in the `showDecorationList()` function.
  - \<d=underline\> | \<d=underline,italic\>
- r
  - Will reset back to default, you can also specify what to reset and provide a list (but only accepts t,b,d).
  - \<r\> | \<r=td\>
- nl
  - Indicates a newline (basically doing `\n`)
  - \<nl\>
