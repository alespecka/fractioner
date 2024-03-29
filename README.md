# Fractioner
### The fraction calculator for life

Fractioner is your everyday command-line tool for manipulation with your fractions!

## Features

Fractioner supports
- all trendy operations, i.e. addition, subtraction, multiplication and division,
- whole numbers, fractions, improper fractions and even mixed fractions as operands,
- grouping with parentheses,
- built-in variable ```ans```, which contains the result of the previous expression.

## Prerequisites

* [Python 3](https://www.python.org/)

## Installation

Either download or clone this repository with the following command and you are good to go.

```
git clone https://github.com/alespecka/fractioner.git
```

## Start application
Navigate to the directory containing Fractioner using command line of your choice and run the command
```
python3 fractioner.py
```
or
```
python fractioner.py
```
depending on which command links to Python 3 on your system. Now you can start typing expressions and Fractioner will evaluate them. For help type ```help```. To exit the application type ```exit```.

To get command-line help run:
```
python3 fractioner.py -h
```
Fractioner also offers a test mode by running:
```
python3 fractioner.py -t
```
The idea here is that each expression is evaluated both as fractions and decimal numbers and the results are compared. If the difference between the two results is less than 10^-12, we call it a success.

To run the unit tests execute:
```
python3 -m unittest
```

## Input
After running Fractioner we can start typing expressions to be evaluated. An expression is valid only if it follows these rules:
* Four operators are supported +, -, *, /.
* Operands may be whole numbers, fractions or mixed fractions.
* Mixed fractions are represented by whole_numerator/denominator, e.g. "1_2/3".
* Operators and operand must be separated by one or more spaces.
* Any number of pairs of parentheses may be included.
* Parentheses do not need to be separated by spaces from operators or operands.
* There is a single variable ```ans```, which contains the result of the last expression.

## Examples
Here is an example run:
```
? 1/2 + 1/3 - 2
= -1_1/6
? (2_3/4 - 1_1/5) * 5
= 7_3/4
? ((1 - 3) - (5/3 + 1/3)) * (2_3/8 + 9/8) / 1/2
= -28
? ans / -7
= 4
```
As you can see above, we may use ```ans``` variable, which stores the result of the previous expression.
