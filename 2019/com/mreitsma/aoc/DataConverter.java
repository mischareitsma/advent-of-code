package com.mreitsma.aoc;

import java.util.Arrays;

public class DataConverter {
    private DataConverter() {}

    public static int[] stringToIntArray(String str, String delimiter) {
        return Arrays.stream(str.split(delimiter)).mapToInt(Integer::parseInt).toArray();
    }
}
