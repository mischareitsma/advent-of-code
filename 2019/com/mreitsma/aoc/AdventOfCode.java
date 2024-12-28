package com.mreitsma.aoc;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.Period;
import java.util.List;

public class AdventOfCode {

    protected final List<String> input;
    protected final boolean isTest;
    private final int day;
    private final int testVersion;

    private String part1;
    private String part2;

    private LocalDateTime totalStartTime;
    private LocalDateTime part1StartTime;
    private LocalDateTime part2StartTime;
    private LocalDateTime totalEndTime;

    public AdventOfCode(int day, boolean isTest) {
        this(day, isTest, 0);
    }

    public AdventOfCode(int day, boolean isTest, int testVersion) {
        this.isTest = isTest;
        this.day = day;
        this.testVersion = testVersion;

        String fileName = String.format("day%02d", this.day);
        if (isTest) {
            fileName += "_test" + (this.testVersion == 0 ? "" : "_" + testVersion);
        }
        fileName += ".dat";

        input = DataReader.readDataFromFile(fileName);
    }

    // Default to no-op for these three
    protected void processInput() {};
    protected void part1() {};
    protected void part2() {};

    public final void run() {
        this.totalStartTime = LocalDateTime.now();
        this.processInput();
        this.part1StartTime = LocalDateTime.now();
        this.part1();
        this.part2StartTime = LocalDateTime.now();
        this.part2();
        this.totalEndTime = LocalDateTime.now();
        this.printResult();
    }

    public void setPart1(String part1) {
        this.part1 = part1;
    }

    public void setPart1(int i) {
        this.setPart1(String.valueOf(i));
    }

    public void setPart2(String part2) {
        this.part2 = part2;
    }

    public void setPart2(int i) {
        this.setPart2(String.valueOf(i));
    }

    public void printResult() {
        String part1Time = (this.part1StartTime != null && this.part2StartTime != null)
                ? getElapsedSecondsAsString(this.part1StartTime, this.part2StartTime)
                : "unknown";
        String part2Time = (this.part2StartTime != null && this.totalEndTime != null)
                ? getElapsedSecondsAsString(this.part2StartTime, this.totalEndTime)
                : "unknown";
        String totalTime = (this.totalStartTime != null && this.totalEndTime != null)
                ? getElapsedSecondsAsString(this.totalStartTime, this.totalEndTime)
                : "unknown";
        System.out.println(
                "Running day " + this.day + ", running as test: " + this.isTest + ", test version: " + this.testVersion
                + ", total runtime: " + totalTime
        );
        System.out.printf("Part1: %s, runtime: %s\n", this.part1, part1Time);
        System.out.printf("Part2: %s, runtime: %s\n", this.part2, part2Time);
    }

    private static String getElapsedSecondsAsString(LocalDateTime startTime, LocalDateTime endTime) {
        return String.format("%.3f", Duration.between(startTime, endTime).toMillis() / 1000.0);
    }
}
