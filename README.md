# VU-Amsterdam Timetable Converter ⏰

Tool to convert VU-Amsterdam timetables (from [rooster.vu.nl](https://rooster.vu.nl)) to `.ics` calendar files, letting you finally add all those events into your calendar.

## Prerequisites
1. Java 8

## Usage
1. Download the latest JAR release of this repo.
2. Run it from the commandline with `java -jar <name-of-jar> "course name"`
    * The `"course name"` is the search term we use to query the timetable system for your course (case insensitive). The first result for that course name search term is picked automatically, so make sure the search term corresponds to the official name of the course. If your course name has multiple words in it, surround it with double-quotes.
3. Your calendar file is waiting for you in this directory, called `output.ics`! Import it into the calendar of your choice!

## Disclaimer
No guarantee of completeness or correctness is provided for this software, see `LICENSE` for details.
