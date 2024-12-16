import os, io, sys, math, json, base64, unittest
from collections.abc import Mapping
from random import Random
from typing import Any, Literal, cast
from functools import partial

from .typing import (
    MISSING, PRESENT, FridBeing, FridError, FridMixin, FridValue, FridNameArgs, StrKeyMap, ValueArgs,
    get_func_name, get_type_name, get_qual_name
)
from .chrono import DateTimeDiff, DateTimeSpec, parse_datetime, parse_timeonly, strfr_datetime
from .chrono import dateonly, timeonly, datetime, timezone, timedelta
from .chrono import murky36_to_datetime, datetime_to_murky36
from ._basic import FridCompare, FridReplace, frid_redact, frid_random
from ._dumps import dump_args_str, dump_frid_tio, dump_frid_str
from ._loads import FridParseError, load_frid_str, load_frid_tio, open_frid_tio, scan_frid_str
from .dotenv import read_dotenv

class TestChrono(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse_datetime("2021-02-03"), dateonly(2021, 2, 3))
        self.assertEqual(parse_datetime("2021-02-03T11:22"), datetime(2021, 2, 3, 11, 22))
        self.assertEqual(parse_datetime("2021-02-03T11:22:33"),
                         datetime(2021, 2, 3, 11, 22, 33))
        self.assertEqual(parse_datetime("2021-02-03T11:22:33.1"),
                         datetime(2021, 2, 3, 11, 22, 33, 100000))
        self.assertEqual(parse_datetime("2021-02-03T112233.12"),
                         datetime(2021, 2, 3, 11, 22, 33, 120000))
        self.assertEqual(parse_datetime("2021-02-03T11:22:33.123"),
                         datetime(2021, 2, 3, 11, 22, 33, 123000))
        self.assertEqual(parse_datetime("2021-02-03T11:22:33.12345"),
                         datetime(2021, 2, 3, 11, 22, 33, 123450))
        self.assertEqual(parse_datetime("2021-02-03T112233.123456"),
                         datetime(2021, 2, 3, 11, 22, 33, 123456))
        self.assertEqual(parse_datetime("2021-02-03T11:22:33.1234567"),
                         datetime(2021, 2, 3, 11, 22, 33, 123456))
        self.assertEqual(parse_datetime("2021-02-03T11:22:33.12Z"),
                         datetime(2021, 2, 3, 11, 22, 33, 120000, timezone.utc))
        self.assertEqual(parse_datetime("11:22:33+00:00"),
                         timeonly(11, 22, 33, tzinfo=timezone(-timedelta())))
        self.assertEqual(parse_datetime("0T11:22-0530"),
                         timeonly(11, 22, tzinfo=timezone(-timedelta(hours=5, minutes=30))))
        self.assertEqual(parse_datetime("0T11:22:33.12+04:30"),
                         timeonly(11, 22, 33, 120000, timezone(timedelta(hours=4, minutes=30))))
        self.assertEqual(parse_datetime("0T112233.12+0430"),
                         timeonly(11, 22, 33, 120000, timezone(timedelta(hours=4, minutes=30))))
        # Not matching cases
        self.assertIsNone(parse_datetime(""))
        self.assertIsNone(parse_datetime("0t11"))
        self.assertIsNone(parse_timeonly("0T11,2233.12+0430"))
        self.assertIsNone(parse_timeonly("11-22-33"))

    def test_strfr(self):
        self.assertEqual(strfr_datetime(dateonly(2011, 2, 13)), "2011-02-13")
        self.assertEqual(strfr_datetime(timeonly(10, 20, 30)), "0T102030.000")
        self.assertEqual(strfr_datetime(timeonly(10, 20, 30), colon=True), "0T10:20:30.000")
        self.assertEqual(strfr_datetime(timeonly(10, 20, 30, 22, timezone.utc)),
                         "0T102030.220Z")
        self.assertEqual(strfr_datetime(datetime(2011, 2, 3, 11, 22, 33, 456789)),
                         "2011-02-03T112233.456")
        self.assertEqual(strfr_datetime(datetime(
            2011, 2, 3, 11, 22, 33, 456789, timezone(timedelta(hours=5, minutes=30))
        ), colon=True), "2011-02-03T11:22:33.456+0530")
        self.assertEqual(strfr_datetime(timeonly(11, 22, 33), precision=1), "0T112233.0")
        self.assertEqual(strfr_datetime(timeonly(11, 22, 33), precision=0), "0T112233")
        self.assertEqual(strfr_datetime(timeonly(11, 22, 33), precision=-1), "0T1122")
        self.assertEqual(strfr_datetime(timeonly(11, 22, 33), precision=-2), "0T11")
        self.assertEqual(strfr_datetime(0),
                         strfr_datetime(datetime.fromtimestamp(0, timezone.utc)))
        with self.assertRaises(ValueError):
            strfr_datetime(timeonly(11, 22, 33), precision=-3)

    def test_fancy36(self):
        # Pure random testing
        start_ts = datetime(2020, 1, 1).timestamp()
        period = datetime(2020, 12, 31, 23, 59, 59, 999999).timestamp() - start_ts
        rng = Random()
        for _ in range(256):
            dt = datetime.fromtimestamp(rng.random() * period + start_ts)
            s = datetime_to_murky36(dt)
            self.assertEqual(len(s), 10)
            self.assertEqual(murky36_to_datetime(s), dt, s)

    def test_datetimediff(self):
        self.assertEqual(dump_frid_str(DateTimeSpec("MON")), "DateTimeSpec(MON)")
        self.assertEqual(dump_frid_str(DateTimeSpec("TUE+1", "2mo")),
                         "DateTimeSpec(+2mo, TUE+)")
        self.assertEqual(dump_frid_str(DateTimeSpec("1h3m", "WED-", month=2)),
                         "DateTimeSpec(+1h3m, WED-, month=2)")
        self.assertEqual(dump_frid_str(DateTimeSpec("+1h3m", "THU+2", day=2)),
                         "DateTimeSpec(+1h3m, THU+2, day=2)")
        self.assertEqual(dump_frid_str(DateTimeSpec("SUN-4", "")),
                         "DateTimeSpec(SUN-4)")
        self.assertEqual(DateTimeDiff("1m3h") + DateTimeDiff("+2m4d"), DateTimeDiff("+3m3h4d"))
        self.assertEqual(str(DateTimeDiff("1year2month3days4hours5minutes6.3125seconds")),
                         "+1yr2mo3d4h5m6.3125s")
        self.assertEqual(dateonly(2020, 1, 3) + DateTimeDiff("+1yr1mo"), dateonly(2021, 2, 3))
        self.assertEqual(dateonly(2020, 1, 3) + DateTimeDiff("+1.0yr1.2mo"), dateonly(2021, 2, 9))
        self.assertEqual(dateonly(2020, 1, 3) - DateTimeDiff("+1yr1mo"), dateonly(2018, 12, 3))
        self.assertEqual(dateonly(2020, 1, 3) + DateTimeDiff("-4d"), dateonly(2019, 12, 30))
        self.assertEqual(dateonly(2020, 5, 30) + DateTimeDiff("+3d20mo"), dateonly(2022, 2, 2))
        self.assertEqual(timeonly(12, 34, 56) + DateTimeDiff("+1h10m10s"), timeonly(13, 45, 6))
        self.assertEqual(timeonly(2, 4, 6) - DateTimeDiff("+10m"), timeonly(1, 54, 6))
        self.assertEqual(
            DateTimeDiff("0.000001s").add_to_timeonly(timeonly(23, 59, 59, 999999)),
            (timeonly(0, 0, 0), 1)
        )
        self.assertEqual(datetime(2020, 5, 30, 22, 50, 10) + DateTimeDiff("1mo1d1h15m55.7s"),
                         datetime(2020, 7, 2, 0, 6, 5, 700000))
        with self.assertRaises(TypeError):
            assert object() + DateTimeDiff("1d")

    def test_datetimespec(self):
        self.assertFalse(DateTimeSpec())
        self.assertTrue(DateTimeSpec("+1s"))
        self.assertTrue(DateTimeSpec(hour=4))
        self.assertTrue(DateTimeSpec("TUE"))
        self.assertEqual(dateonly(2020, 2, 4) + DateTimeSpec("+1m3h"), dateonly(2020, 2, 4))
        self.assertEqual(timeonly(10, 2, 4) + DateTimeSpec(), timeonly(10, 2, 4))
        self.assertEqual(timeonly(10, 2, 4) + DateTimeSpec("+1m3h"), timeonly(13, 3, 4))
        self.assertEqual(datetime(2020, 2, 4) + DateTimeSpec("+1m3h"),
                         datetime(2020, 2, 4, 3, 1))
        self.assertEqual(datetime(2020, 2, 4, 10, 55, 3) + DateTimeSpec(
            - DateTimeDiff("-1mo1d"), month=6, time="03:05:20"
        ), datetime(2020, 7, 5, 3, 5, 20))
        self.assertEqual(datetime(2020, 2, 4, 10, 55, 3) + DateTimeSpec(
            - DateTimeDiff("-1mo1d"), month=6, time="0T030520", minute=6, microsecond=100
        ), datetime(2020, 7, 5, 3, 6, 20, 100))
        self.assertEqual(datetime(2020, 2, 4, 10, 55, 3) + DateTimeSpec(
            - DateTimeDiff("-1mo1d"), month=6, time="T0305", hour=4, second=7
        ), datetime(2020, 7, 5, 4, 5, 7))
        self.assertEqual(DateTimeSpec(month=5).add_to_dateonly(dateonly(2024, 7, 1), 1),
                         dateonly(2025, 5, 1))
        self.assertEqual(DateTimeSpec(month=5).add_to_dateonly(dateonly(2024, 7, 1), -1),
                         dateonly(2024, 5, 1))
        self.assertEqual(DateTimeSpec(month=6).add_to_dateonly(dateonly(2024, 5, 31), 1),
                         dateonly(2024, 7, 1))
        self.assertEqual(DateTimeSpec(month=6).add_to_dateonly(dateonly(2024, 5, 31), -1),
                         dateonly(2023, 7, 1))
        self.assertEqual(DateTimeSpec(day=29).add_to_dateonly(dateonly(2023, 3, 28), -1),
                         dateonly(2023, 3, 1))
        self.assertEqual(DateTimeSpec(week=2).add_to_dateonly(dateonly(2023, 5, 7)),
                         dateonly(2023, 1, 9))
        self.assertEqual(DateTimeSpec(week=1, day=3).add_to_dateonly(dateonly(2024, 5, 7)),
                         dateonly(2024, 1, 3))
        self.assertEqual(DateTimeSpec(
            year=2024, month=4, week=1, day=4
        ).add_to_dateonly(dateonly.today()), dateonly(2024, 4, 4))
        self.assertEqual(DateTimeSpec(
            year=2024, month=5, week=2, day=1
        ).add_to_dateonly(dateonly.today()), dateonly(2024, 5, 13))
        self.assertEqual(DateTimeSpec(minute=5).add_to_timeonly(timeonly(20, 30, 40), 1),
                         (timeonly(21, 5, 40), 0))
        self.assertEqual(DateTimeSpec(minute=30).add_to_timeonly(timeonly(20, 30, 40), -1),
                         (timeonly(20, 30, 40), 0))
        self.assertEqual(DateTimeSpec(minute=30).add_to_timeonly(timeonly(0, 10, 40), -1),
                         (timeonly(23, 30, 40), -1))
        self.assertEqual(DateTimeSpec(second=30).add_to_timeonly(timeonly(23, 59, 59), 1),
                         (timeonly(0, 0, 30), 1))
        self.assertEqual(DateTimeSpec(microsecond=0).add_to_timeonly(timeonly(23, 59, 59, 1), 1),
                         (timeonly(0, 0, 0), 1))
        self.assertEqual(DateTimeSpec(month=10).add_to_timeonly(timeonly(12, 34, 56, 7890), -1),
                         (timeonly(12, 34, 56, 7890), 0))
        # 2024-07-25 is a Thursay
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("FRIDAY"), dateonly(2024, 7, 26))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("THU"), dateonly(2024, 7, 25))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("WED"), dateonly(2024, 7, 24))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("FRI+"), dateonly(2024, 7, 26))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("THU+"), dateonly(2024, 7, 25))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("WED+"), dateonly(2024, 7, 31))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("FRI-"), dateonly(2024, 7, 19))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("THU-"), dateonly(2024, 7, 25))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("WED-"), dateonly(2024, 7, 24))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("FRI+1"), dateonly(2024, 7, 26))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("THU+1"), dateonly(2024, 7, 25))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("WED+2"), dateonly(2024, 8, 7))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("FRI-1"), dateonly(2024, 7, 19))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("THU-1"), dateonly(2024, 7, 25))
        self.assertEqual(dateonly(2024, 7, 25) + DateTimeSpec("WED-2"), dateonly(2024, 7, 17))
        # Mixed
        self.assertEqual(dateonly(2024, 1, 1) + DateTimeSpec("+2d", month=7, day=23, weekday=2),
                         dateonly(2024, 7, 24))
        self.assertEqual(timeonly(20, 30, 40) + DateTimeSpec("-2m", hour=4, second=20),
                         timeonly(4, 28, 20))
        self.assertEqual(DateTimeSpec(hour=8, minute=9).add_to_datetime(
            datetime(2020, 1, 1, 10, 20, 30), 1
        ), datetime(2020, 1, 2, 8, 9, 30))
        self.assertEqual(datetime(2020, 3, 4, 5, 6, 7, 800000)
                         + DateTimeSpec("-20h", year=2024, minute=9, microsecond=20),
                         datetime(2024, 3, 3, 9, 9, 7, 20))
        self.assertEqual(datetime(2020, 4, 5, 6, 7, 8, 999999)
                         + DateTimeSpec("FRI-", "+0.1s", date="2024-07-25"),
                         datetime(2024, 7, 19, 6, 7, 9, 99999))
        with self.assertRaises(TypeError):
            assert object() + DateTimeSpec()

class TestBasic(unittest.TestCase):
    def test_comparator(self):
        cmp = FridCompare()
        self.assertTrue(cmp(None, None))
        self.assertTrue(cmp(2, 2))
        self.assertFalse(cmp(1, "1"))
        # Unsupported data type
        self.assertFalse(cmp(cast(FridValue, self), cast(FridValue, self)))
        data = ['a', '1', 1, datetime.now(), b"345"]
        self.assertTrue(cmp(data, data))
        self.assertFalse(cmp(data, 'a'))
        self.assertFalse(cmp(data, 3))
        data = {'a': [1, True, 2.0, None, False], 'b': "Hello", 'c': [
            dateonly.today(), datetime.now(), datetime.now().time()
        ]}
        self.assertTrue(cmp(data, data))
        self.assertFalse(cmp(data, 'a'))
        self.assertFalse(cmp(data, 3))

    def test_comparator_submap(self):
        cmp = FridCompare(compare_dict=FridCompare.is_submap)
        self.assertTrue(cmp({'a': 1}, {'a': 1, 'b': 2}))
        self.assertFalse(cmp({'a': 1}, {'a': 3, 'b': 2}))
        self.assertFalse(cmp({'a': 1}, {}))
        self.assertFalse(cmp({'a': 1}, 3))

    def test_substitute(self):
        sub = FridReplace(present="+.", missing="-.")
        self.assertEqual(sub(3), 3)
        self.assertEqual(sub("${a}", a=MISSING), "-.")
        self.assertEqual(sub("${a}", a=PRESENT), "+.")
        self.assertEqual(sub("[${a}]", a=MISSING), "[-.]")
        self.assertEqual(sub("[${a}]", a=PRESENT), "[+.]")
        self.assertEqual(sub("${a}"), "-.")
        self.assertEqual(sub("a"), "a")
        self.assertEqual(sub("The ${key}=${val} is here", {'key': "data", 'val': 3}),
                         "The data=3 is here")
        self.assertEqual(sub("The ${var} is here", var="data"), "The data is here")
        self.assertEqual(sub({
            'a': "${var1}", 'b': ["${var2}", "${var3}"]
        }, var1=3, var2=['abc', 4], var3='def'), {
            'a': 3, 'b': ['abc', 4, 'def']
        })
        self.assertEqual(sub(["${var1}", "${var2}"], var1=PRESENT, var2=MISSING), ["+.", "-."])
        with self.assertRaises(ValueError):
            sub("abc ${def")
        # This is for the pattern
        self.assertEqual(sub("${var*}", var1="x", var2="y"), {'1': "x", '2': "y"})
        self.assertEqual(sub("[${va*}]", var1="x", var2="y"), "[{r1: x, r2: y}]")

    def test_type_check(self):
        self.assertEqual(get_type_name(FridBeing), "FridBeing")
        self.assertEqual(get_type_name(PRESENT), "FridBeing")
        self.assertEqual(get_type_name(MISSING), "FridBeing")
        self.assertEqual(get_qual_name(FridBeing), "FridBeing")
        self.assertEqual(get_qual_name(PRESENT), "FridBeing")
        self.assertEqual(get_qual_name(MISSING), "FridBeing")
        self.assertEqual(get_func_name(self.test_type_check), "test_type_check(...)")
        self.assertEqual(get_func_name(id), "id(...)")
        def test(a, b, c):
            pass
        self.assertEqual(get_func_name(test), "test(...)")
        self.assertIsInstance(partial(test, 3), partial)
        self.assertEqual(get_func_name(partial(test)), "test(...)")
        self.assertEqual(get_func_name(partial(test, 3)), "test(3,...)")
        self.assertEqual(get_func_name(partial(test, b=3)), "test(...,b=3,...)")


class TestLoadsAndDumps(unittest.TestCase):
    common_cases = {
        "123": 123,     " 123 ": 123,   "-4": -4,       "   -4   ": -4,
        "0.0": 0.0,     "+0.0": 0.0,    "+0.": 0.0,     ".0": 0.0,
        "-0.0": -0.0,   "-0.": -0.0,    "-.0": -0.0,    "-0.00": -0.0,
        "0.5": 0.5,     "+0.5": 0.5,    "5E-1": 0.5,    "+0.05e1": 0.5,
        "-0.5": -0.5,   "-.5": -0.5,    "-5E-1": -0.5,  "-0.05e1": -0.5,
        "-2.0": -2.0,   "-2.": -2.0,    "-2E0": -2.0,   "-.2E1": -2.0,
        '""': '',       '   ""  ': '',
        "\"\\u20af\"": "\u20aF",        "\"\\u20aF\" ": "\u20af",
        "[]": [],       "[   ] ": [],
        "[\"\"]": [''],                 "[,] ": [''],
        "[1]": [1],     "[ 1]": [1],    "[ 1 , ] ": [1],
        "[1, 2]": [1,2],                " [ 1 ,   2]": [1,2],
        "{}": {},       "{   }": {},
    }
    json_only_cases = {
        "{\"a\": 1, \"b\": 2}": {'a': 1, 'b': 2},
        "{\"a\": 1, \"b\": 2,   }": {'a': 1, 'b': 2},
    }
    json_json5_cases = {
        "null": None,   " null ": None, "  null": None, "    null    ": None,
        "true": True,   "  true": True, "false": False, "false  ": False,
        '"a"': "a",
    }
    json5_only_cases = {
        "+Infinity": math.inf,          "Infinity": math.inf,           "-Infinity": -math.inf,
        "NaN": math.isnan,              "+NaN": math.isnan,             "-NaN": math.isnan,
        '"b"': "b",     "'b'": "b",
    }
    frid_json5_cases = {
        "3": 3,         "0x3": 3,       "-19": -19,     "-0X13": -19,
        '""': "",       "''": "",
        '"abc\\r\\ndef"': "abc\r\ndef", "'abc\\r\\ndef'": "abc\r\ndef",
        "{a: 3}": {'a': 3},             "{ a : 3 ,}": {'a': 3},
        "{ 'a' : 3}": {'a':3},
        '{",": "}"}': {',': "}"},       "{ ',': '}' }": {',': "}"},
        "{a: 1, b: 2}": {'a': 1, 'b': 2},               "{a: 1, b: 2,  }": {'a': 1, 'b': 2},
    }
    frid_only_cases = {
        # Constants
        ".": None,      " . ": None,    ". ": None,     " .  ": None,
        "+": True,      " +": True,     "-": False,     "- ": False,
        # Numbers
        "30": 30,       " 3_0 ": 30,    "2000": 2000,   " +2_000 ": 2000,
        "12345": 12345, "1_2_3_4_5": 12345,
        "-400000": -400000,             "-400_000  ": -400000,
        "0.25": 0.25,   ".25": 0.25,    "2.5E-1": 0.25,
        "++": math.inf, "--": -math.inf, "+-": math.isnan, "-+": math.isnan,
        # Unquoted strings
        '""': '',       "": '',         " ": '',        "  ": '',
        "c": "c",       "'c'": "c",     '"c"': "c",     "  `c`  ": "c",
        "abc": "abc",   " abc ": "abc", " `abc` ": "abc",
        "ab d": "ab d", " ab d ": "ab d",
        '"ab  e"': "ab  e",
        "user@admin.com": "user@admin.com",
        # Quoted strings
        '" a\\eb"': " a\033b",    "  `\\x20a\\eb`": " a\033b",
        '"\\U00010248"': "\U00010248",  " '\\U00010248' ": "\U00010248",
        '"\\e\\e\\"\'` "': "\033\033\"'` ",
        "  '\\e\\x1b\\\"\\'\\` '": "\033\033\"'` ",
        # "'''tester's test''' """: "tester's test", # Do not support triple quotes yet
        # Blob
        "..": b'',      " ..": b'',         ".. ": b'',
        "..YQ": b"a", "..YWI": b"ab",    "..YWJj": b"abc",
        # List
        "[3, [4, 6], abc, [\"\"], [[[]]]]": [3,[4,6],"abc",[''],[[[]]]],
        "[3, [4, 6], abc , [,], [[[]]],  ] ": [3,[4,6],"abc",[''],[[[]]]],
        # Dict
        "{a.b: c, _: \"[]\", d+e-f: g@h}": {'a.b': "c", '_': "[]", 'd+e-f': "g@h"},
        "{a.b: c, _: '[]', d+e-f: g@h  , }": {'a.b': "c", '_': "[]", 'd+e-f': "g@h"},
        "{: \"\"}": {'': ''}, "{:}": {'': ''}, "{: a}": {'': "a"}, "{:a}": {'': "a"},
        # Set: Python caveats: True == 1 and False == 0; also
        "{,}": set(), "{a}": {'a'}, "{3}": {3}, "{+}": {True}, "{-}": {False}, "{.}": {None},
        # Can't set multi value set, since set is not following insert ordering
        "{0,1,2,.}": (lambda x: x == {0, 1, 2, None}),

        # "()": (''), "(a>3)": LionExprStub('a>3'),
        # "(([{()}]))": LionExprStub("([{()}])"),
        # "(x in [a,b,c])": LionExprStub("x in [a,b,c]"),
        # "(x in '([{\\'\"\\\"')": LionExprStub("x in '([{\\'\"\\\"'"),
        # TODO: do we support non-string keys"{.:+}": {None: True}
    }
    def _do_test_positive(self, cases: StrKeyMap, json_level: Literal[0,1,5]):
        prev_value = ...
        for i, (s, t) in enumerate(cases.items()):
            try:
                v = load_frid_str(s, json_level=json_level)
                if callable(t):
                    self.assertTrue(t(v), f"[{i}] {s} ==> {t} ({json_level=})")
                    continue
                self.assertEqual(t, v, f"[{i}] {s} ==> {t} ({json_level=})")
                assert t is not ...
                if t == prev_value:
                    continue
                assert not isinstance(t, FridBeing)
                self.assertEqual(s, dump_frid_str(t, json_level=json_level),
                                f"[{i}] {s} <== {t} ({json_level=})")
                # With loose mode
                v1 = load_frid_str(s, json_level=json_level, loose_mode=True)
                self.assertEqual(v, v1)
                # With indentation
                s1 = dump_frid_str(t, json_level=json_level, indent='\t')
                v = load_frid_str(s1, json_level=json_level)
                if callable(t):
                    self.assertTrue(t(v), f"[{i}] {s} ==> {t} ({json_level=})")
                else:
                    self.assertEqual(t, v, f"[{i}] {s} ==> {t} ({json_level=})")
            except Exception:
                print(f"\nError @ [{i}] {s} <=> {t} ({json_level=})", file=sys.stderr)
                raise
            prev_value = t
    def test_positive(self):
        self._do_test_positive(self.common_cases, 0)
        self._do_test_positive(self.common_cases, 1)
        self._do_test_positive(self.common_cases, 5)
        self._do_test_positive(self.json_only_cases, 1)
        self._do_test_positive(self.json5_only_cases, 5)
        self._do_test_positive(self.json_json5_cases, 1)
        self._do_test_positive(self.json_json5_cases, 5)
        self._do_test_positive(self.frid_json5_cases, 0)
        self._do_test_positive(self.frid_json5_cases, 5)
        self._do_test_positive(self.frid_only_cases, 0)
        self.assertEqual(dump_frid_str(math.nan), "+-")
        self.assertEqual(dump_frid_str(-math.nan), "-+")
        self.assertEqual(dump_frid_str(math.nan, json_level=5), "NaN")

    def test_random(self):
        def_seed = 0
        def_runs = 64
        def_tree = 4
        runs = int(os.getenv('FRID_RANDOM_RUNS', def_runs))
        seed = os.getenv('FRID_RANDOM_SEED')
        if seed is None:
            seed = def_seed
        else:
            seed = load_frid_str(seed)
            assert isinstance(seed, int|float|bytes|str)
        tree = int(os.getenv('FRID_RANDOM_TREE', def_tree))

        if seed != def_seed or runs != def_runs or tree != def_tree:
            print(f"\nRunning random test with {runs} rounds, seed={seed}")
        rng = Random()
        rng.seed(seed)

        for _ in range(runs):
            r = rng.randint(0, 15)
            dump_args = {
                'print_real': None if r & 1 else lambda x: format(x, '+'),
                'print_date': None if r & 2 else lambda v: strfr_datetime(v, precision=6),
                'print_blob': None if r & 4 else lambda v: base64.b16encode(v).decode(),
                'ascii_only': bool(r & 8),
            }
            load_args = {
                'parse_real': None if r & 1 else lambda s: (
                    int(s, 0) if s[1:].isnumeric() and (s[0].isnumeric() or s[0] in "+-")
                    else float(s)
                ),
                'parse_date': None if r & 2 else lambda s: parse_datetime(s),
                'parse_blob': None if r & 4 else lambda s: base64.b16decode(s),
            }
            # Test with only JSON compatible values
            data = frid_random(rng, tree, for_json=1)
            text = json.dumps(data)
            self.assertEqual(data, load_frid_str(text, json_level=1), msg="Loading JSON")
            self.assertEqual(data, load_frid_str(text, json_level=5), msg="Loading JSON5")
            for json_level in (0, 1, 5):
                s = dump_frid_str(data, json_level=json_level, **dump_args)
                self.assertEqual(data, load_frid_str(s, json_level=json_level, **load_args),
                                 msg=f"{json_level=} {len(s)=}")
            # Test with only JSON-5 compatible values
            data = frid_random(rng, tree, for_json=5)
            for json_level in (0, 5):
                s = dump_frid_str(data, json_level=json_level, **dump_args)
                self.assertEqual(data, load_frid_str(s, json_level=json_level, **load_args),
                                 msg=f"{json_level=} {len(s)=}")
            # Test with only all possible frid values
            json_level: Literal[0,1,5] = rng.choice([0, 1, 5])
            for escape_seq in ('~', "#!"):
                data = frid_random(rng, tree, for_json=0)
                s = dump_frid_str(data, json_level=json_level,
                                  escape_seq=escape_seq, **dump_args)
                self.assertEqual(data, load_frid_str(
                    s, json_level=1, escape_seq=escape_seq, **load_args
                ), msg=f"{len(s)=}")
                t = io.StringIO()
                dump_frid_tio(data, t, json_level=json_level,
                              escape_seq=escape_seq, **dump_args)
                self.assertEqual(s, t.getvalue())
                self.assertEqual(data, load_frid_tio(
                    io.StringIO(s), rng.randint(1, 5), json_level=1, escape_seq=escape_seq,
                    **load_args
                ), msg=f"{len(s)=}")
                # With loose mode
                self.assertEqual(data, load_frid_tio(
                    io.StringIO(s), rng.randint(1, 5), json_level=1, escape_seq=escape_seq,
                    loose_mode=True, **load_args
                ), msg=f"{len(s)=}")
                # With indentitation and lineends
                s = dump_frid_str(data, json_level=json_level, indent=4,
                                  escape_seq=escape_seq, **dump_args)
                self.assertEqual(data, load_frid_str(
                    s, json_level=json_level, escape_seq=escape_seq, **load_args
                ), msg=f"{len(s)=}")
                self.assertEqual(data, load_frid_tio(
                    io.StringIO(s), 64, json_level=json_level, escape_seq=escape_seq,
                    **load_args
                ), msg=f"{len(s)=}")

    negative_load_cases = [
        # Numbers
        "3+7", "4 x 2", "  .5abc", "-6d ef  ", ".723 ghi 4", "+abc", "-invalid",
        "3_", "+_", "0x-", "0x_",
        # Strings
        "I'm here", "back`ticks`", "a\\ b ", " c(d)", "Come, here",
        "'No ending quote", "'''Mismatched end quote' '", "'wrong quotes`",
        "'\\", "'\\x2", "'\\x3'", "'\\x9k'", "'\\u37'", "'\\xyz'", "'\\U03'",
        # List
        "[1,", "[}",
        # Dict
        "{a:3,,}", "{)", "{a:1, a:2}", "{3a:3}", "{3: 4}",
        # Set
        "{3, a:}", "{b:3, +}"
        # Expr
        "(", "([})", "((())",
    ]
    def test_negative_load(self):
        # print(f"Running {len(positive_testcases)} negative testcases...")
        for i, k in enumerate(self.negative_load_cases):
            with self.assertRaises(FridParseError, msg=f"[{i}]: {k}"):
                load_frid_str(k)


    negative_json_dump_cases = [
        math.nan, math.inf, -math.inf, dateonly.today(), b"1234", {3: 4}, object(),
    ]
    def test_negative_json_dump(self):
        for i, k in enumerate(self.negative_json_dump_cases):
            with self.assertRaises(ValueError, msg=f"[{i}]: {k}"):
                dump_frid_str(k, json_level=1)

    expression_cases = {
        "()": "", "(())": "()", "(')')": "')'",
        "{a:(')'), b: (['()[]{}'])}": {'a': "')'", 'b': "['()[]{}']"}
    }
    def test_expression(self):
        for i, (k, v) in enumerate(self.expression_cases.items()):
            w = load_frid_str(k, parse_expr=(lambda x, p: x))
            self.assertEqual(v, w, msg=f"[{i}]: {k}")

    comment_cases = {
        "\n123": 123, "\n[\n123,\n\n 456,]": [123, 456],
        "123 # 456": 123, "123 # 456\n": 123, "// abc\n456": 456, "/* abc */ 123": 123,
        "[123, #456,\n789]": [123, 789], "[1,/*1,\n3,*/ 4 // 5,\n # 6\n, 7]": [1,4,7],
    }
    def test_comments(self):
        for i, (k, v) in enumerate(self.comment_cases.items()):
            w = load_frid_str(k, comments=["#", "//", ("/*", "*/")])
            self.assertEqual(v, w, msg=f"[{i}]: {k}")

    scan_cases = {
        "123\n456": (123, "456"),
        "123 // 456\n789": (123, "789"),
        "123 /* 456 */\t\n789": (123, "789"),
        "123 /* 456 */ 789\n": Exception,
    }
    def test_scan(self):
        kwargs: dict[str,Any] = dict(comments=["//", ("/*", "*/")])
        for s, t in self.scan_cases.items():
            if isinstance(t, type) and issubclass(t, BaseException):
                with self.assertRaises(t):
                    scan_frid_str(s, 0, until_eol=True, **kwargs)
                with self.assertRaises(t):
                    open_frid_tio(io.StringIO(s), **kwargs)(
                        until_eol=True
                    )
                continue
            assert isinstance(t, tuple)
            (data, trailing) = t
            (value, index) = scan_frid_str(s, 0, until_eol=True, **kwargs)
            self.assertEqual(data, value, f"{s=}")
            self.assertEqual(s[index:], trailing, f"{s=}")
            value = open_frid_tio(io.StringIO(s), **kwargs)(until_eol=True)
            self.assertEqual(data, value, f"{s=}")

    class TestMixinClass(FridMixin):
        def __init__(self, *args, **kwds):
            super().__init__()
            self._args = args
            self._kwds = kwds
        def frid_repr(self, **kwargs) -> FridNameArgs:
            return FridNameArgs(get_type_name(self), self._args, self._kwds)
        def __repr__(self):
            return dump_args_str(self.frid_repr())
        def __eq__(self, other):
            if self is other:
                return True
            if not isinstance(other, __class__):
                return False
            return self._args == other._args and self._kwds == other._kwds
    class TestMixinClass2(TestMixinClass):
        def __init__(self, *args, opt, **kwds):
            super().__init__(*args, **kwds)
            self._opt = opt
        @classmethod
        def frid_from(cls, data: FridNameArgs, /, *, opt, **kwargs):
            return cls(*data.args, opt=opt, **data.kwds)
        def frid_repr(self, *, opt, **kwargs) -> FridNameArgs:
            assert opt == self._opt
            return super().frid_repr()
        def __eq__(self, other):
            if not super().__eq__(other):
                return False
            return self._opt == other._opt

    def test_mixins(self):
        test = self.TestMixinClass()
        frid = "TestMixinClass()"
        self.assertEqual(dump_frid_str(test), frid)
        self.assertEqual(load_frid_str(frid, frid_mixin=[self.TestMixinClass]), test)
        json = '"#!TestMixinClass()"'
        self.assertEqual(dump_frid_str(test, json_level=1, escape_seq="#!"), json)
        self.assertEqual(load_frid_str(
            json, frid_mixin=[self.TestMixinClass], json_level=1, escape_seq="#!"
        ), test)

        test = self.TestMixinClass("Test", a=3)
        frid = "TestMixinClass(Test, a=3)"
        self.assertEqual(dump_frid_str(test), frid)
        self.assertEqual(load_frid_str(frid, frid_mixin=[self.TestMixinClass]), test)
        json = """{"": ["#!TestMixinClass", "Test"], "a": 3}"""
        self.assertEqual(dump_frid_str(test, json_level=1, escape_seq="#!"), json)
        self.assertEqual(load_frid_str(
            json, frid_mixin=[self.TestMixinClass], json_level=1, escape_seq="#!"
        ), test)

        test = self.TestMixinClass2("Test", opt=2, a=3)
        frid = "TestMixinClass2(Test, a=3)"
        value_args: ValueArgs[type[FridMixin]] = ValueArgs(self.TestMixinClass2, opt=2)
        self.assertEqual(dump_frid_str(test, mixin_args=[value_args]), frid)
        self.assertEqual(load_frid_str(frid, frid_mixin=[value_args]), test)
        json = """{"": ["#!TestMixinClass2", "Test"], "a": 3}"""
        self.assertEqual(dump_frid_str(test, mixin_args=[value_args],
                                       json_level=1, escape_seq="#!"), json)
        self.assertEqual(load_frid_str(
            json, frid_mixin=[value_args], json_level=1, escape_seq="#!"
        ), test)

    def test_frid_error(self):
        data = {'error': FridError("Test")}
        s = dump_frid_str(data)
        self.assertEqual(s, "{error: FridError(Test)}")
        t = load_frid_str(s, frid_mixin=[FridError])
        self.assertTrue(isinstance(t, Mapping) and isinstance(t.get('error'), FridError))

    def test_identation(self):
        data = {'x': ["a", "b", []], 'y': 2, 'z': self.TestMixinClass(3, 4, b=5)}
        s = ("{\n\tx: [\n\t\ta,\n\t\tb,\n\t\t[\n\t\t]?\n\t],\n"
             "\ty: 2,\n\tz: TestMixinClass(3, 4, b=5)?\n}\n")
        self.assertEqual(
            dump_frid_str(data, indent='\t'),
            s.replace('?', '')
        )
        self.assertEqual(
            dump_frid_str(data, indent='\t', extra_comma=True),
            s.replace('?', ',')
        )
        data = {'a': "abc", 'b': "abc\n", 'c': "abc\ndef", 'd': "abc\ndef\n", 'e': [
            "abc", "abc\n", "abc\ndef", "abc\ndef\n", "abc\ndef\nghi", "abc\ndef\nghi\n",
        ]}
        # With break quotes
        s = dump_frid_str(data, indent='\t', break_quoted=True)
        self.assertEqual(data, load_frid_str(s), s)
        s = dump_frid_str(data, indent='\t', break_quoted=True, extra_comma=True)
        self.assertEqual(data, load_frid_str(s), s)

    def test_redact(self):
        now = datetime.now()
        self.assertEqual(frid_redact({
            'a': 3, 'b': ["ab", b"a", now, now.time(), 3.5, self.TestMixinClass()],
            'c': [], 'd': False, 'e': None, 'f': PRESENT,
        }), {
            'a': 'i', 'b': ['s2', 'b1', 'd', 't', 'f', 'TestMixinClass'], 'c': [], 'd': False,
            'e': None, 'f': PRESENT
        })
        self.assertEqual(frid_redact({
            'a': 3, 'b': ["a", "b", "c"], 'c': [], 'd': False, 'e': None,
        }, 0), {
            'a': PRESENT, 'b': [3], 'c': [], 'd': PRESENT, 'e': PRESENT,
        })

class TestDotenv(unittest.TestCase):
    def test_read_dotenv(self):
        data = [x.lstrip()  for x in """# This is a test dotenv file
        A = 4
        B=3
        C   ="first
        second"
        D=    "ab${B}c"
        E = "---
        multiline
        ---"
        """.splitlines(keepends=True)]
        self.assertEqual(read_dotenv(data), {
            'A': "4", 'B': '3', 'C': "first\nsecond", 'D': "ab3c",
            'E': "---\nmultiline\n---",
        })
