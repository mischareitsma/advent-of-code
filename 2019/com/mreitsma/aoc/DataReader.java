package com.mreitsma.aoc;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class DataReader {
    private DataReader() {}

    private static final Path dataPath = Paths.get(System.getProperty("user.dir"), "data");

    public static List<String> readDataForDay(int day) {
        return readDataFromFile(Paths.get(dataPath.toString(), String.format("day%02d.dat", day)));
    }

    public static List<String> readDataForDay(int day, int version) {
        return readDataFromFile(Paths.get(dataPath.toString(), String.format("day%02d_%d.dat", day, version)));
    }

    public static List<String> readTestDataForDay(int day) {
        return readDataFromFile(Paths.get(dataPath.toString(), String.format("day%02d_test.dat", day)));
    }

    public static List<String> readTestDataForDay(int day, int version) {
        return readDataFromFile(Paths.get(dataPath.toString(), String.format("day%02d_test_%d.dat", day, version)));
    }

    private static List<String> readDataFromFile(Path path) {
        try {
            return Files.readAllLines(path);
        } catch (IOException iox) {
            throw new RuntimeException(iox);
        }
    }
}
