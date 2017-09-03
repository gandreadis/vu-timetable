package com.gandreadis.vutimetable.crawler;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.logging.Level;
import java.util.logging.Logger;

final class Navigator {
    private static final Logger LOGGER = Logger.getLogger(Navigator.class.getName());

    private final Crawler crawler;
    private final WebDriver driver;

    Navigator(final Crawler crawler) {
        this.crawler = crawler;
        driver = crawler.getDriver();
    }

    void navigate() {
        LOGGER.log(Level.INFO, "Navigating to rooster.vu.nl");
        driver.get("https://rooster.vu.nl/");

        LOGGER.log(Level.INFO, "Switching to the 'module' tab");
        navigateToModulesTab();
        LOGGER.log(Level.INFO, "Searching for your course and selecting it");
        selectCourse();
        LOGGER.log(Level.INFO, "Selecting the option outputting one semester worth of events");
        selectSemester();
        LOGGER.log(Level.INFO, "Navigating to the timetable page");
        navigateToTimetable();
    }

    private void navigateToModulesTab() {
        driver.findElement(By.id("LinkBtn_modules")).click();
    }

    private void selectCourse() {
        driver.findElement(By.id("tWildcard")).sendKeys(crawler.getCourseName());
        driver.findElement(By.id("bWildcard")).click();
        driver.findElement(By.id("dlObject")).findElement(By.tagName("option")).click();
    }

    private void selectSemester() {
        final WebElement selectElement = driver.findElement(By.id("lbWeeks"));
        for (WebElement option : selectElement.findElements(By.tagName("option"))) {
            if (option.getText().toLowerCase().contains("semester")) {
                option.click();
                return;
            }
        }
    }

    private void navigateToTimetable() {
        driver.findElement(By.id("bGetTimetable")).click();
    }
}
