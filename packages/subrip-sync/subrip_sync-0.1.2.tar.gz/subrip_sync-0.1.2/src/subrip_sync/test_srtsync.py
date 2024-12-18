import unittest
from . import subrip

class TestSubRipMethods(unittest.TestCase):
    def test_parse_timecode(self):
        tc = '23:12:04,657'
        timestamp = 23 * 3600_000 + 12 * 60_000 + 4 * 1000 + 657
        self.assertEqual(subrip.parse_timecode(tc), timestamp)

    def test_strf_timestamp(self):
        timestamp = 23 * 3600_000 + 12 * 60_000 + 4 * 1000 + 657
        tc = '23:12:04,657'
        self.assertEqual(subrip.strf_timestamp(timestamp), tc)

    def test_strf_timestamp_big(self):
        timestamp = 223 * 3600_000 + 2 * 60_000 + 4 * 1000 + 57
        tc = '223:02:04,057'
        self.assertEqual(subrip.strf_timestamp(timestamp), tc)

    def test_process_timecode(self):
        tc1 = '01:02:14,949'
        tc2 = '01:02:19,131'
        lag = 4182
        self.assertEqual(subrip.process_timecode(tc1, lag), tc2)

    def test_process_line(self):
        line = '...01:02:04,999 --> 01:12:02,057...'
        lag = 64002
        result = '...01:03:09,001 --> 01:13:06,059...'
        self.assertEqual(subrip.process_line(line, lag), result)

    def test_process_doc(self):
        doc1 = '''
1
00:01:24,210 --> 00:01:25,503
"Apocalypse 21.

2
00:01:27,588 --> 00:01:29,840
"Je vis un nouveau Ciel.

'''
        doc2 = '''
1
00:01:24,330 --> 00:01:25,623
"Apocalypse 21.

2
00:01:27,708 --> 00:01:29,960
"Je vis un nouveau Ciel.

'''
        self.assertEqual(subrip.process_document(doc1.splitlines(keepends=True), 120), doc2)