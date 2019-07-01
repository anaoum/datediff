# DateDiff

datediff counts the number of whole days between two events. Dates must range
between 01/01/1901 and 31/12/2999 (inclusive). The order of dates passed as
command-line arguments does not matter (i.e. the calculation is symmetrical).
The number of whole days between the same dates and successive dates is zero.

## Requirements
Python3

## Usage
```
datediff.py [-h] [--date-fmt DATE_FMT] date1 date2

positional arguments:
  date1                the date of the first event
  date2                the date of the second event

optional arguments:
  -h, --help           show this help message and exit
  --date-fmt DATE_FMT  the format of dates passed as command-line arguments
                       (default: DD/MM/YYYY)
```

## Implementation

### Motivation
Our approach was motivated by the goal of finding a constant time (i.e.
non-iterative) solution.

### Approach

Calculate the number of days between each date and some epoch and then subtract
these two numbers. To ensure the calculation is symmetrical, we take the
absolute value of this subtraction. We also subtract 1 from non-zero results to
only count whole days. We chose 01/01/0001 as the epoch since it simplified
calculations.

To calculate the number of days between a given date and the epoch, first we
calculate the day relative to the year of a given date. For example: the first
of January is the first day of the year; the first of February is the 32nd day
of the year; the first of March is 60th day of the year in non-leap years; the
first of March is the 61st day of the year in leap years; and so on.

After calculating the day of the year given a date, we add all the days of the
previous years. This is equal to `(year-1)*365` plus all the leap days in the
previous years. We calculate the number of leap days in the previous years as:
`(year-1)//4 - (year-1)//100 + (year-1)//400`. Note the use of integer division.

## Testing
Some sanity-checking doctest tests are present in datediff.py and are executed
each time the script is called.

To run the unit tests, execute:
```
python3 datediff_test.py
```

The unit tests include the examples from the problem description, some manually
created tests cases, as well as randomly generated test cases that use Python's
datetime library to validate our datediff implementation.

## Copyright

Copyright 2019 Andrew Naoum

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
