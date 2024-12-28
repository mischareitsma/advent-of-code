package com.mreitsma.aoc.aoc2019.solutions;

import com.mreitsma.aoc.AdventOfCode;
import com.mreitsma.aoc.DataReader;

import java.util.List;

public class Day01 extends AdventOfCode {

    // TODO: This should be fixed, also copy/paste. Reflection is a thing I think?
    public Day01(int day, boolean isTest) {
        super(day, isTest);
    }

    public static void main(String[] args) {
        System.out.println(System.getProperty("user.dir"));
        new Day01(1, false).run();
    }

    public final void part1() {
        this.setPart1(input.stream()
                .map(String::trim)
                .map(Double::parseDouble)
                .map((d) -> Math.floor(d/3) - 2)
                .mapToInt(Double::intValue).sum());
    }

    public final void part2() {
        this.setPart2(input.stream()
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
                .mapToInt(Double::intValue).sum());
    }
}
