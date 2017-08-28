# VU Timetable

Tool to convert VU timetables (from [rooster.vu.nl](https://rooster.vu.nl)) to `.ics` calendar files, letting you finally add all those events into your calendar.

## Prerequisites
1. Git
2. Python >=3.3

## Usage
1. Clone this repo.
2. Run `python setup.py install`
3. Generate your timetable per course/module in [rooster.vu.nl](https://rooster.vu.nl). Be sure to select **Type of Report** to be `Module` when generating the table.
4. Once you are on the HTML page generated for you, hit <kbd>Ctrl-S</kbd> to save the page. To make sure you don't download only the HTML code, select 'HTML only' in the 'save as type' dropdown. Save the file in the cloned directory of this repo, under the name `input.html`.
5. Run `python main.py` from this directory.
6. Your calendar file is waiting for you in this directory, called `output.ics` 🎉
