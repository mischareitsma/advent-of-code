package com.mreitsma.aoc.aoc2019.solutions;

import com.mreitsma.aoc.AdventOfCode;
import java.util.*;

public class Day03 extends AdventOfCode {

    private final List<int[]> path1 = new ArrayList<>();
    private final List<int[]> path2 = new ArrayList<>();
    private static final Map<Character, int[]> dirs = new HashMap<>();

    static {
        dirs.put('L', new int[]{-1, 0});
        dirs.put('R', new int[]{1, 0});
        dirs.put('U', new int[]{0, 1});
        dirs.put('D', new int[]{0, -1});
    }

    public Day03(int day, boolean isTest, int testVersion) {
        super(day, isTest, testVersion);
    }

    public static void main(String[] args) {
        new Day03(3, false, 3).run();
    }

    @Override
    protected void processInput() {
        generatePath(path1, input.getFirst());
        generatePath(path2, input.getLast());


    }

    private void generatePath(List<int[]> path, String directions) {
        path.add(new int[]{0, 0, 0});
        int[] curr = {0, 0};
        int steps = 0;

        for (String movement : directions.split(",")) {
            int[] dir = dirs.get(movement.charAt(0));
            int len = Integer.parseInt(movement.substring(1));
            for (int i = 0; i < len; i++) {
                curr[0] += dir[0];
                curr[1] += dir[1];
                steps++;
                path.add(new int[]{curr[0], curr[1], steps});
            }
        }
    }

    @Override
    protected void part1() {
        // does part 1 and 2 in one.
        int shortest_distance = Integer.MAX_VALUE;
        int shortest_steps = Integer.MAX_VALUE;

        for (int[] pos1 : path1) {
            for (int[] pos2 : path2) {
                if (pos1[0] == 0 && pos1[1] == 0)
                    continue;
                if (pos1[0] != pos2[0] || pos1[1] != pos2[1])
                    continue;

                int mh = Math.abs(pos1[0]) + Math.abs(pos1[1]);
                if (mh < shortest_distance)
                    shortest_distance = mh;

                int steps = pos1[2] + pos2[2];
                if (steps < shortest_steps) {
                    shortest_steps = steps;
                }
            }
        }

        setPart1(shortest_distance);
        setPart2(shortest_steps);
    }
}

