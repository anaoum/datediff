import unittest
from datetime import date, timedelta
import random

from datediff import datediff

MIN_YEAR = 1901
MAX_YEAR = 2999

class DateDiffTest(unittest.TestCase):

    def _test(self, date1, date2, expected=None, symmetrical=True):
        """Tests the datediff function for the given dates. date1 and date2
        should be instances of datetime.date. If no expected value is provided,
        one will be calculated using datetime operations. If symmetrical is
        True, the test will be performed in both directions (i.e. both
        datediff(date1, date2) and datediff(date2, date1) will be tested.)
        """
        if expected is None:
            expected = date2 - date1
            expected = abs(expected.days)
            if expected != 0:
                expected -= 1
        if symmetrical:
            self._test(date2, date1, expected, False)
        date1 = date1.strftime("%d/%m/%Y")
        date2 = date2.strftime("%d/%m/%Y")
        actual = datediff(date1, date2, "DD/MM/YYYY")
        self.assertEqual(actual, expected, \
                msg="{}–{} should be {}".format(date1, date2, expected))

    # Problem description
    def test_eg1(self):
        self._test(date(1983, 6, 2), date(1983, 6, 22), 19)
    def test_eg2(self):
        self._test(date(1984, 7, 4), date(1984, 12, 25), 173)
    def test_eg3(self):
        self._test(date(1989, 1, 3), date(1983, 8, 3), 1979)
    def test_eg4(self):
        self._test(date(2018, 8, 3), date(2018, 8, 4), 0)
    def test_eg5(self):
        self._test(date(2000, 1, 1), date(2000, 1, 3), 1)

    # Zero days
    def test_same_date(self):
        self._test(date(2000, 1, 1), date(2000, 1, 1), 0)
    def test_successive_dates(self):
        self._test(date(2000, 1, 1), date(2000, 1, 2), 0)

    # Ordinary years
    def test_same_month(self):
        self._test(date(1993, 1, 2), date(1993, 1, 31))
    def test_same_year(self):
        self._test(date(1993, 1, 2), date(1993, 12, 31))
    def test_many_years(self):
        self._test(date(1993, 1, 1), date(1995, 12, 31))
    def test_divisible_by_100(self):
        self._test(date(2100, 1, 1), date(2100, 12, 31))
        self._test(date(2097, 1, 1), date(2103, 12, 31))

    # Leap years
    def test_leap_in_one(self):
        self._test(date(1992, 1, 2), date(1995, 3, 4))
    def test_leap_in_both(self):
        self._test(date(1992, 5, 6), date(1996, 7, 8))
    def test_leap_in_middle(self):
        self._test(date(1993, 9, 10), date(1997, 11, 12))
    def test_leap_in_many(self):
        self._test(date(1992, 12, 13), date(1997, 1, 14))
        self._test(date(1988, 2, 15), date(1996, 3, 16))
        self._test(date(1980, 2, 15), date(1996, 3, 16))
    def test_divisible_by_400(self):
        self._test(date(2000, 1, 1), date(2000, 12, 31))
        self._test(date(1997, 1, 1), date(2003, 12, 31))
        self._test(date(1996, 1, 1), date(2004, 12, 31))

    # Ranges
    def test_max_range(self):
        self._test(date(1901, 1, 1), date(2999, 12, 31))
    def test_min_date(self):
        self._test(date(1901, 1, 1), date(1902, 1, 1))
    def test_max_date(self):
        self._test(date(2998, 12, 31), date(2999, 12, 31))

    # Randomly generated
    @staticmethod
    def random_date_in_year(year):
        is_leap = year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)
        if is_leap:
            offset = random.randrange(0, 366)
        else:
            offset = random.randrange(0, 365)
        return date(year, 1, 1) + timedelta(days=offset)
    def test_random_dates(self, days_per_year=1):
        for year1 in range(MIN_YEAR, MAX_YEAR+1):
            for _ in range(days_per_year):
                date1 = self.random_date_in_year(year1)
                for year2 in range(MIN_YEAR, MAX_YEAR+1):
                    for _ in range(days_per_year):
                        date2 = self.random_date_in_year(year2)
                        self._test(date1, date2)

    # Format
    def test_default_fmt(self):
        self.assertEqual(datediff("03/01/1989", "03/08/1983"), 1979)
    def test_dmy_fmt(self):
        self.assertEqual(datediff("03/01/1989", "03/08/1983", date_fmt="DD/MM/YYYY"), 1979)
    def test_mdy_fmt(self):
        self.assertEqual(datediff("01/03/1989", "08/03/1983", date_fmt="MM/DD/YYYY"), 1979)
    def test_ymd_fmt(self):
        self.assertEqual(datediff("1989-01-03", "1983-08-03", date_fmt="YYYY-MM-DD"), 1979)

    # Invalid dates
    def _test_raises(self, date1, date2, exception, exception_message=None, symmetrical=True):
        with self.assertRaises(exception) as cm:
            datediff(date1, date2)
        if exception_message is not None:
            self.assertEqual(exception_message, str(cm.exception))
        if symmetrical:
            self._test_raises(date2, date1, exception, exception_message, False)
    def test_invalid_date(self):
        self._test_raises("01/1/2100", "01/01/2000", ValueError)
        self._test_raises("1/01/2100", "01/01/2000", ValueError)
        self._test_raises("01/01/00", "01/01/2000", ValueError)
        self._test_raises("2010-01-01", "01/01/2000", ValueError)
        self._test_raises("01/Jan/2100", "01/01/2000", ValueError)
    def test_invalid_day(self):
        self._test_raises("00/01/2100", "01/01/2000", ValueError, "cannot parse date: invalid day")
        self._test_raises("32/01/2100", "01/01/2000", ValueError, "cannot parse date: invalid day")
        self._test_raises("29/02/2100", "01/01/2000", ValueError, "cannot parse date: invalid day")
        self._test_raises("30/02/2000", "01/01/2000", ValueError, "cannot parse date: invalid day")
        self._test_raises("31/04/2100", "01/01/2000", ValueError, "cannot parse date: invalid day")
    def test_invalid_month(self):
        self._test_raises("01/00/2000", "01/01/2000", ValueError, "cannot parse date: invalid month")
        self._test_raises("01/01/2000", "01/13/2000", ValueError, "cannot parse date: invalid month")
    def test_invalid_year(self):
        self._test_raises("31/12/1900", "01/01/1901", ValueError, "cannot parse date: invalid year")
        self._test_raises("01/01/3000", "31/12/2999", ValueError, "cannot parse date: invalid year")

if __name__ == "__main__":
    random.seed(0)
    unittest.main()
