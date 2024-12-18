import re

def parse_timecode(timecode):
    factors = [3600_000, 60_000, 1000, 1]
    l1, l2 = [e.split(':') for e in timecode.split(',')]
    values = [int(e) for e in l1 + l2]
    return sum([i * j for (i, j) in zip(factors, values)])

def strf_timestamp(timestamp):
    milliseconds = timestamp % 1000
    seconds = timestamp // 1000 % 60
    minutes = timestamp // 60_000 % 60
    hours = timestamp // 3600_000
    return f'{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}'

def process_timecode(timecode, lag):
    timestamp = parse_timecode(timecode)
    return strf_timestamp(timestamp + lag)

pattern = re.compile(r'\d+:\d{2}:\d{2},\d{3}')
def process_line(line, lag):
    return pattern.sub(lambda m: process_timecode(m.group(0), lag), line)

def process_document(lines, lag):
    return ''.join(process_line(line, lag) for line in lines)