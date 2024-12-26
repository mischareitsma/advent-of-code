package com.mreitsma.aoc.aoc2019.solutions;

import com.mreitsma.aoc.DataReader;

import java.util.List;

public class Day01 {
    private static final boolean isTest = false;

    private final List<String> input;

    public static void main(String[] args) {
        System.out.println(System.getProperty("user.dir"));
        new Day01().run();
    }

    public Day01() {
        input = isTest ? DataReader.readTestDataForDay(1) : DataReader.readDataForDay(1);
    }

    public final void run() {
        System.out.println(part1());
        System.out.println(part2());
    }

    public final int part1() {
        return input.stream()
                .map(String::trim)
                .map(Double::parseDouble)
                .map((d) -> Math.floor(d/3) - 2)
                .mapToInt(Double::intValue).sum();
    }

    public final int part2() {
        return input.stream()
                .map(String::trim)
                .map(Double::parseDouble)
                .map((d) -> {
                    double curr = Math.floor(d/3) - 2;
                    double tot = curr;
                    while (curr >= 9) {
                        curr = Math.floor(curr/3) - 2;
                        tot += curr;
                    }
                    return tot;
                })
                .mapToInt(Double::intValue).sum();
    }
}
