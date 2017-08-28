import datetime
import re

from bs4 import BeautifulSoup
from ics import Calendar, Event


def main():
    with open("input.html", encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    calendar = get_calendar(soup)

    with open('output.ics', 'w') as output_file:
        output_file.writelines(calendar)


def get_calendar(soup):
    calendar = Calendar()

    entries = soup.select('table tr')

    for entry in entries:
        if re.search('\d+/\d+/\d+', str(entry)) is None or not re.search('Printdatum', str(entry)) is None:
            continue

        start_date = datetime.datetime.strptime(nth(entry, 2), "%d/%m/%y")
        start_time_ints = nth(entry, 4).split(':')
        start_time_delta = datetime.timedelta(hours=int(start_time_ints[0]), minutes=int(start_time_ints[1]))
        end_time_ints = nth(entry, 5).split(':')
        end_time_delta = datetime.timedelta(hours=int(end_time_ints[0]), minutes=int(end_time_ints[1]))

        weeks = get_weeks(nth(entry, 3))

        for week in weeks:
            event = Event()
            event.name = "{} - {}".format(nth(entry, 6), nth(entry, 8))
            event.location = "VU - {}".format(nth(entry, 9))
            event.description = "Vakcode: {}\nDocent: {}".format(nth(entry, 1), nth(entry, 10))
            event.begin = start_date + datetime.timedelta(days=(7 * week)) + start_time_delta
            event.end = start_date + datetime.timedelta(days=(7 * week)) + end_time_delta

            calendar.events.append(event)

    return calendar


def nth(soup, n):
    return soup.select_one('td:nth-of-type({})'.format(n)).get_text()


def get_weeks(ranges):
    result = []
    for part in ranges.split(','):
        if '-' in part:
            a, b = part.split('-')
            a, b = int(a), int(b)
            result.extend(range(a, b + 1))
        else:
            a = int(part)
            result.append(a)

    if len(result) > 0:
        for index in range(1, len(result)):
            result[index] = result[index] - result[0]
        result[0] = 0

    return result


if __name__ == "__main__":
    main()
