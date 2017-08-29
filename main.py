import datetime
import re

from bs4 import BeautifulSoup
from ics import Calendar, Event
from pytz import timezone

AMS_TIMEZONE = timezone('Europe/Amsterdam')


def main():
    """
    Reads the file called "input.html" in this directory and outputs a corresponding calendar file called "output.ics".
    """
    with open('input.html', encoding='utf8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    calendar = get_calendar(soup)

    with open('output.ics', 'w') as output_file:
        output_file.writelines(calendar)


def get_calendar(soup):
    """
    Parses the HTML document represented by the BeautifulSoup instance and returns a calendar with events of that page.

    :param soup: the BeautifulSoup instance of the page to be parsed.
    :return: a calendar instance populated with the parsed events.
    """

    calendar = Calendar()

    rows = soup.select('table tr')

    for row in rows:
        if re.search('\d+/\d+/\d+', str(row)) is None or not re.search('Printdatum', str(row)) is None:
            continue

        events = convert_row_to_events(row)
        calendar.events.extend(events)

    return calendar


def convert_row_to_events(row):
    """
    Scrapes the given row for event information and returns a list of events that row represents.

    :param row: the BeautifulSoup instance of one <tr> element.
    :return: a list of events encoded by that row.
    """

    nth_column = lambda n: row.select_one('td:nth-of-type({})'.format(n)).get_text()

    start_date = datetime.datetime.strptime(nth_column(2), '%d/%m/%y')
    start_time_ints = nth_column(4).split(':')
    start_time_delta = datetime.timedelta(hours=int(start_time_ints[0]), minutes=int(start_time_ints[1]))
    end_time_ints = nth_column(5).split(':')
    end_time_delta = datetime.timedelta(hours=int(end_time_ints[0]), minutes=int(end_time_ints[1]))

    weeks = convert_ranges_to_weeks(nth_column(3))

    events = []

    for week in weeks:
        event = Event()
        event.name = '{} - {}'.format(nth_column(6), nth_column(8))
        event.location = 'VU - {}'.format(nth_column(9))
        event.description = 'Vakcode: {}\nDocent: {}'.format(nth_column(1), nth_column(10))
        event.begin = AMS_TIMEZONE.localize(start_date + datetime.timedelta(days=(7 * week)) + start_time_delta)
        event.end = AMS_TIMEZONE.localize(start_date + datetime.timedelta(days=(7 * week)) + end_time_delta)

        events.append(event)

    return events


def convert_ranges_to_weeks(ranges):
    """
    Takes the given week ranges and returns normalized weeks in those ranges.

    Example: "10-12, 14" evaluates to [0, 1, 2, 4]

    :param ranges: string representing one or more week ranges.
    :return: a normalized list representation of those ranges.
    """
    weeks = []
    for part in ranges.split(','):
        if '-' in part:
            start, end = part.split('-')
            start, end = int(start), int(end)
            weeks.extend(range(start, end + 1))
        else:
            week = int(part)
            weeks.append(week)

    # Normalize relative to first week
    if len(weeks) > 0:
        for index in range(1, len(weeks)):
            weeks[index] = weeks[index] - weeks[0]
        weeks[0] = 0

    return weeks


if __name__ == "__main__":
    main()
