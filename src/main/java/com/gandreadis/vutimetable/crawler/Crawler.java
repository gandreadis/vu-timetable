package com.gandreadis.vutimetable.crawler;

import biweekly.ICalendar;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.htmlunit.HtmlUnitDriver;
import org.openqa.selenium.remote.BrowserType;
import org.openqa.selenium.remote.DesiredCapabilities;

public final class Crawler implements AutoCloseable {
    private final String courseName;
    private final HtmlUnitDriver driver;

    public Crawler(final String courseName) {
        this.courseName = courseName;
        DesiredCapabilities capabilities = DesiredCapabilities.htmlUnit();
        capabilities.setVersion(BrowserType.FIREFOX);
        driver = new HtmlUnitDriver(capabilities);
    }

    public ICalendar getCalendar() {
        new Navigator(this).navigate();
        return new Parser(this).parse();
    }

    String getCourseName() {
        return courseName;
    }

    WebDriver getDriver() {
        return driver;
    }

    @Override
    public void close() throws Exception {
        driver.close();
    }
}
