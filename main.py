import datetime
import re
import sys

from bs4 import BeautifulSoup
from ics import Calendar, Event
from pytz import timezone
from selenium import webdriver

AMS_TIMEZONE = timezone('Europe/Amsterdam')


def main():
    """
    Fetches a course timetable and outputs a corresponding calendar file called "output.ics".
    """
    if len(sys.argv) != 2:
        print('Usage; python main.py "course name"')
        return

    print('Retrieving your timetable page from rooster.vu.nl...')
    html_source = get_html(sys.argv[1])

    print('Parsing the page for timetable events...')
    soup = BeautifulSoup(html_source, 'html.parser')

    calendar = get_calendar(soup)

    with open('output.ics', 'w') as output_file:
        output_file.writelines(calendar)

    print('Your calendar file should be ready for you, look for "output.ics" in this folder!')


def get_html(course_name):
    browser = webdriver.Chrome()
    browser.get('https://rooster.vu.nl/')

    # Go to 'modules' page
    browser.find_element_by_id('LinkBtn_modules').click()

    # Select course options
    browser.find_element_by_id('tWildcard').send_keys(course_name)
    browser.find_element_by_id('bWildcard').click()
    browser.find_element_by_id('dlObject').find_element_by_tag_name('option').click()
    print('test')
    select_option(browser, 'lbWeeks', 'Semester')

    # Go to 'modules' page
    browser.find_element_by_id('bGetTimetable').click()

    html_source = browser.page_source
    browser.close()

    return html_source


def select_option(browser, id, text):
    select_element = browser.find_element_by_id(id)
    lowercase_text = text.lower()

    for option in select_element.find_elements_by_tag_name('option'):
        if lowercase_text in option.text.lower():
            option.click()
            break


def get_calendar(soup):
    """
    Parses the HTML document represented by the BeautifulSoup instance and returns a calendar with events of that page.

    :param soup: the BeautifulSoup instance of the page to be parsed.
    :return: a calendar instance populated with the parsed events.
    """

    calendar = Calendar()

    rows = soup.select('table.spreadsheet tr')

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
