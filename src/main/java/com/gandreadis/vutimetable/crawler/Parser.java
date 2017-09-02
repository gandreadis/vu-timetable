package com.gandreadis.vutimetable.crawler;

import biweekly.ICalendar;
import biweekly.component.VEvent;
import org.apache.commons.lang3.time.DateUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

final class Parser {
    private static final Pattern DATE_PATTERN = Pattern.compile("\\d+/\\d+/\\d+");

    private final SimpleDateFormat dateFormat = new SimpleDateFormat("d/M/yy");
    private final WebDriver driver;

    Parser(final Crawler crawler) {
        driver = crawler.getDriver();
    }

    ICalendar parse() {
        final ICalendar calendar = new ICalendar();
        final List<WebElement> rows = driver.findElements(By.cssSelector("table.spreadsheet tr")).stream()
                .filter(row -> !row.getText().contains("Printdatum")
                        && DATE_PATTERN.matcher(getInnerHTML(row)).find())
                .collect(Collectors.toList());

        for (WebElement row : rows) {
            try {
                calendar.getEvents().addAll(getRowEvents(row));
            } catch (ParseException e) {
                e.printStackTrace();
            }
        }

        return calendar;
    }

    private String getInnerHTML(final WebElement element) {
        return (String) ((JavascriptExecutor) driver).executeScript("return arguments[0].innerHTML;", element);
    }

    private List<VEvent> getRowEvents(final WebElement row) throws ParseException {
        final List<WebElement> columns = row.findElements(By.tagName("td"));

        final Date startDateMidnight = dateFormat.parse(columns.get(1).getText());
        final int[] startTime = splitInts(columns.get(3).getText(), ":");
        final int[] endTime = splitInts(columns.get(4).getText(), ":");
        final List<Integer> weeks = convertRangesToWeeks(columns.get(2).getText());

        final List<VEvent> events = new ArrayList<>();
        weeks.forEach(week -> {
            final VEvent event = new VEvent();
            event.setSummary(columns.get(5).getText() + " - " + columns.get(7).getText());
            event.setLocation("VU Amsterdam - " + columns.get(8).getText());
            event.setDescription("Vakcode: " + columns.get(0).getText()
                    + "\nDocent: " + columns.get(9).getText());
            event.setDateStart(addTimeDelta(startDateMidnight, 7 * week, startTime[0], startTime[1]));
            event.setDateEnd(addTimeDelta(startDateMidnight, 7 * week, endTime[0], endTime[1]));
            events.add(event);
        });

        return events;
    }

    private Date addTimeDelta(final Date date, final int days, final int hours, final int minutes) {
        return DateUtils.addDays(
                DateUtils.addMinutes(
                        DateUtils.addHours(
                                date,
                                hours
                        ),
                        minutes
                ),
                days
        );
    }

    private List<Integer> convertRangesToWeeks(final String ranges) {
        final List<Integer> weeks = new ArrayList<>();

        for (String part : ranges.split(",")) {
            if (part.contains("-")) {
                final int[] bounds = splitInts(part, "-");
                weeks.addAll(IntStream.rangeClosed(bounds[0], bounds[1])
                        .boxed().collect(Collectors.toList()));
            } else {
                final int week = Integer.parseInt(part);
                weeks.add(week);
            }
        }

        if (!weeks.isEmpty()) {
            for (int i = 1; i < weeks.size(); i++) {
                weeks.set(i, weeks.get(i) - weeks.get(0));
            }
            weeks.set(0, 0);
        }

        return weeks;
    }

    private int[] splitInts(final String input, final String delimiter) {
        final String[] tokens = input.split(delimiter);
        final int[] parsedTokens = new int[tokens.length];

        for (int i = 0; i < tokens.length; i++) {
            parsedTokens[i] = Integer.parseInt(tokens[i].trim());
        }
        return parsedTokens;
    }
}
