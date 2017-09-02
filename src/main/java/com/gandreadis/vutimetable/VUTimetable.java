package com.gandreadis.vutimetable;

import com.gandreadis.vutimetable.crawler.Crawler;

import java.io.File;

public class VUTimetable {
    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Please provide the name of the course (within double quotes) as argument.");
            return;
        }

        try (Crawler crawler = new Crawler(args[0])) {
            crawler.getCalendar().write(new File("output.ics"));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
