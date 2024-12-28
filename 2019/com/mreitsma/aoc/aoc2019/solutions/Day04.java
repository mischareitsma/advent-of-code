package com.mreitsma.aoc.aoc2019.solutions;

import com.mreitsma.aoc.AdventOfCode;

import java.util.*;

public class Day04 extends AdventOfCode {

    private final int[] testNumbers = new int[] {111111, 122345, 111123, 223450, 123789};
    private final boolean[] testNumberValid = new boolean[] {true, true, true, false, false};

    private int startRange;
    private int endRange;

    public Day04(int day, boolean isTest) {
        super(day, isTest);
    }

    public static void main(String[] args) {
        new Day04(4, false).run();
    }

    @Override
    protected void processInput() {
        String[] digits = input.getFirst().split("-");
        startRange = Integer.parseInt(digits[0]);
        endRange = Integer.parseInt(digits[1]);
    }

    public final void part1() {
        if (this.isTest) {
            for (int i = 0; i < testNumbers.length; i++) {
                System.out.println(
                        "Test number " + testNumbers[i] +
                        ", should be " + testNumberValid[i] +
                        ", is " + isValidPassword(testNumbers[i], false)
                );
            }
            return;
        }

        int validPasswords = 0;

        for (int i = startRange; i < endRange; i++) {
            if (isValidPassword(i, false)) {
                validPasswords++;
            }
        }
        setPart1(validPasswords);
    }

    @Override
    protected final void part2() {
        int validPasswords = 0;
        for (int i = startRange; i < endRange; i++) {
            if (isValidPassword(i, true)) {
                validPasswords++;
            }
        }
        setPart2(validPasswords); // 196 too low
    }

    private boolean isValidPassword(int pwd, boolean hasDouble) {
        Map<Integer,ArrayList<Integer>> digits = new HashMap<Integer,ArrayList<Integer>>();
        String strRepr = String.valueOf(pwd);
        int prevVal = 0;
        for (int i = 0; i < 6; i++) {
            int currVal = Integer.parseInt(strRepr.substring(i, i + 1));
            if (currVal < prevVal)
                return false;

            if (!digits.containsKey(currVal)) {
                digits.put(currVal, new ArrayList<>());
            }
            digits.get(currVal).add(i);
            prevVal = currVal;
        }

        boolean hasRepeating = false;
        boolean hasDoubleRepeating = false;

        for (int i: digits.keySet()) {
            List<Integer> l = digits.get(i);

            if (l.size() == 1)
                continue;

            if (l.size() == 2)
                hasDoubleRepeating = true;

            hasRepeating = true;
        }

        if (hasDouble && !hasDoubleRepeating)
            return false;

        return hasRepeating;
    }
}
