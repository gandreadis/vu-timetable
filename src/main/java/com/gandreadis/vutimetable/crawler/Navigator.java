package com.gandreadis.vutimetable.crawler;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

final class Navigator {
    private final Crawler crawler;
    private final WebDriver driver;

    Navigator(final Crawler crawler) {
        this.crawler = crawler;
        driver = crawler.getDriver();
    }

    void navigate() {
        driver.get("https://rooster.vu.nl/");

        navigateToModulesTab();
        selectCourse();
        selectSemester();
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
