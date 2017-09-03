package com.gandreadis.vutimetable;

import com.gandreadis.vutimetable.crawler.Crawler;

import java.io.File;
import java.util.logging.Level;
import java.util.logging.Logger;

public final class VUTimetable {
    private static final Logger LOGGER = Logger.getLogger(VUTimetable.class.getName());

    static {
        configureLoggers();
    }

    public static void main(String[] args) {
        LOGGER.log(Level.INFO, "\n  vu-timetable\n================\n");

        if (args.length != 1) {
            LOGGER.log(Level.WARNING, "Please provide the name of the course (within double quotes) as argument");
            return;
        }

        try (Crawler crawler = new Crawler(args[0])) {
            crawler.getCalendar().write(new File("output.ics"));
        } catch (Exception e) {
            LOGGER.log(Level.SEVERE, e.getMessage(), e);
        }
    }

    private static void configureLoggers() {
        System.getProperties().setProperty("java.util.logging.SimpleFormatter.format", "%4$s: %5$s%n");
        Logger.getLogger("com.gargoylesoftware.htmlunit").setLevel(Level.SEVERE);
    }
}
