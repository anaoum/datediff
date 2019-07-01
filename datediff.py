#!/usr/bin/env python3

MIN_YEAR = 1901
MAX_YEAR = 2999
DEFAULT_DATE_FORMAT = "DD/MM/YYYY"

def is_leap(year):
    """Return True if the given year is a leap year, False otherwise.
    >>> is_leap(1999)
    False
    >>> is_leap(1996)
    True
    >>> is_leap(2100)
    False
    >>> is_leap(2000)
    True
    """
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False

days_per_month_comm = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
days_per_month_leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def validate(day, month, year):
    """Ensures that the given day, month, and year constitute a valid date in
    the Gregorian calendar, and fall within the minimum and maximum years
    specified by this module.

    If the given day, month, and year are valid, this function returns nothing:
    >>> validate(29, 2, 2000)

    If the given day, month, and year are invalid, this function raises a
    ValueError with the reason why it is invalid:
    >>> validate(29, 2, 2001)
    Traceback (most recent call last):
    ...
    ValueError: invalid day
    >>> validate(1, 13, 2001)
    Traceback (most recent call last):
    ...
    ValueError: invalid month
    >>> validate(1, 1, 3000)
    Traceback (most recent call last):
    ...
    ValueError: invalid year
    """

    if not MIN_YEAR <= year <= MAX_YEAR:
        raise ValueError("invalid year")
    if not 1 <= month <= 12:
        raise ValueError("invalid month")
    if is_leap(year):
        days_per_month = days_per_month_leap[month-1]
    else:
        days_per_month = days_per_month_comm[month-1]
    if not 1 <= day <= days_per_month:
        raise ValueError("invalid day")

def parse(string, date_fmt):
    """Parse a string as a date, returning a day, month, and year tuple. The
    string should be formatted according to date_fmt. date_fmt should contain
    exactly one occurrence of each of DD, MM, and YYYY. For example,
    "1989-01-03" is a valid date adhering to the date_fmt "YYYY-MM-DD":
    >>> parse("1989-01-03", "YYYY-MM-DD")
    (3, 1, 1989)
    >>> parse("2000-01-CC", "YYYY-MM-DD")
    Traceback (most recent call last):
    ...
    ValueError: cannot parse date: invalid literal for int() with base 10: 'CC'
    """
    day_idx = date_fmt.find("DD")
    month_idx = date_fmt.find("MM")
    year_idx = date_fmt.find("YYYY")
    try:
        day = int(string[day_idx:day_idx+2])
        month = int(string[month_idx:month_idx+2])
        year = int(string[year_idx:year_idx+4])
        validate(day, month, year)
        return day, month, year
    except ValueError as e:
        raise ValueError("cannot parse date: " + str(e))

doy_offset_comm = [sum(days_per_month_comm[:i]) for i in range(12)]
doy_offset_leap = [sum(days_per_month_leap[:i]) for i in range(12)]

def day_of_year(day, month, year):
    """Determine the day of a given year, given a day, month, year tuple.
    >>> day_of_year(1, 1, 2000)
    1
    >>> day_of_year(29, 2, 2000)
    60
    """
    if is_leap(year):
        return doy_offset_leap[month-1] + day
    else:
        return doy_offset_comm[month-1] + day

def days_since_epoch(day, month, year):
    """Return the number of days since the epoch, defined as 01/01/0001 to
    simplify calculations.
    >>> days_since_epoch(1, 1, 1)
    0
    >>> days_since_epoch(29, 2, 4)
    1154
    >>> days_since_epoch(1, 1, 1901)
    693960
    """
    doy = day_of_year(day, month, year)
    return doy + (year-1)*365 + (year-1)//4 - (year-1)//100 + (year-1)//400 - 1

def datediff(date1, date2, date_fmt=DEFAULT_DATE_FORMAT):
    """Return the number of whole days between two dates. The order of dates
    does not matter. Dates should be formatted according to date_fmt.
    >>> datediff("03/08/2018", "03/08/2018")
    0
    >>> datediff("03/08/2018", "04/08/2018")
    0
    >>> datediff("02/06/1983", "22/06/1983")
    19
    >>> datediff("04/07/1984", "25/12/1984")
    173
    >>> datediff("03/01/1989", "03/08/1983")
    1979
    >>> datediff("03/08/1983", "03/01/1989")
    1979
    >>> datediff("1989-01-03", "1983-08-03", "YYYY-MM-DD")
    1979
    """
    date1 = parse(date1, date_fmt)
    date2 = parse(date2, date_fmt)
    days = days_since_epoch(*date1) - days_since_epoch(*date2)
    if days != 0:
        days = abs(days) - 1
    return days

if __name__ == "__main__":

    import doctest
    doctest.testmod()

    import argparse

    def date_format(string):
        if string.count("YYYY") != 1 or string.count("MM") != 1 or \
                string.count("DD") != 1:
            raise argparse.ArgumentTypeError("must contain exactly one " \
                    "occurrence of each DD, MM, and YYYY")
        return string

    parser = argparse.ArgumentParser(description="Count the number of whole " \
            "days between two events. Dates must range between 01/01/{} and " \
            "31/12/{}. The order of dates passed as command-line arguments " \
            "does not matter.".format(MIN_YEAR, MAX_YEAR))
    parser.add_argument("date1", help="the date of the first event")
    parser.add_argument("date2", help="the date of the second event")
    parser.add_argument("--date-fmt", default=DEFAULT_DATE_FORMAT, \
            type=date_format, help="the format of dates passed as " \
            "command-line arguments (default: {})".format(DEFAULT_DATE_FORMAT))
    args = parser.parse_args()

    print(datediff(**vars(args)))
