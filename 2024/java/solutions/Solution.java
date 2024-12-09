package solutions;

import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.Stream;

public abstract class Solution {

    private Path filePath;
    private List<String> fileContents;

    private final boolean isTest;
    private final boolean useStrings;

    public Solution(boolean isTest, boolean useStrings) {
        this.isTest = isTest;
        this.useStrings = useStrings;
    }

    public Solution(boolean isTest) {
        this(isTest, false);
    }

    public final void solve() {
        readInput();
        processInput();

        String sol1, sol2;

        if (useStrings) {
            sol1 = stringPart1();
            sol2 = stringPart2();
        }
        else {
            sol1 = Long.toString(part1());
            sol2 = Long.toString(part2());
        }

        System.out.println("Result of part 1: " + sol1);
        System.out.println("Result of part 2: " + sol2);
    }

    private void readInput() {
        try {
            fileContents = Files.readAllLines(filePath, Charset.defaultCharset());
        } catch (IOException ioe) {
            throw new RuntimeException("Failed to read input file", ioe);
        }
    }

    abstract void processInput();

    long part1() {
        return 0;
    }

    long part2() {
        return 0;
    }

    String stringPart1() {
        return "";
    }

    String stringPart2() {
        return "";
    }

    public final List<String> getFileContents() {
        return fileContents;
    }

    public final Stream<String> getFileContentsStream() {
        return getFileContents().stream();
    }
}
