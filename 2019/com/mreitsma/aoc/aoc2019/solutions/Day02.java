package com.mreitsma.aoc.aoc2019.solutions;

import com.mreitsma.aoc.AdventOfCode;
import com.mreitsma.aoc.DataConverter;
import com.mreitsma.aoc.DataReader;

public class Day02 extends AdventOfCode {
    private int[] pgm;
    public static void main(String[] args) {
        new Day02(2, false).run();
    }

    public Day02(int day, boolean isTest) {
        super(day, isTest);
    }

    @Override
    protected final void processInput() {
        this.pgm = DataConverter.stringToIntArray(input.getFirst(), ",");
    }

    @Override
    protected final void part1() {
        setPart1(runProgram(12, 2));
    }

    @Override
    protected final void part2() {
        final int target = 19690720;
        for (int noun = 0; noun <= 99; noun++) {
            for (int verb = 0; verb <= 99; verb++) {
                if (runProgram(noun, verb) == target) {
                    setPart2(100 * noun + verb);
                    return;
                }
            }
        }
    }

    public int runProgram(int noun, int verb) {
        int[] pgm = this.pgm.clone();
        pgm[1] = noun;
        pgm[2] = verb;
        int idx = 0;

        while (pgm[idx] != 99) {
            int opcode = pgm[idx];
            int idx1 = pgm[idx+1];
            int idx2 = pgm[idx+2];
            int idx3 = pgm[idx+3];

            if (opcode == 1) {
                pgm[idx3] = pgm[idx1] + pgm[idx2];
            }
            else if (opcode == 2) {
                pgm[idx3] = pgm[idx1] * pgm[idx2];
            }
            idx += 4;
        }

        return pgm[0];
    }
}
