package util;

import java.util.Arrays;
import java.util.List;

/**
 * Input Transformation Class.
 * This class has some useful transformation methods to get the data from the input in a
 * particular format.
 */
public class InputTransformer {

    private InputTransformer() {}

    public static List<Long> getInputStringAsListOfLongs(String input, String delim) {
        return Arrays.stream(input.split(delim)).map(Long::parseLong).toList();
    }

    public static List<Double> getInputStringAsListOfDoubles(String input, String delim) {
        return Arrays.stream(input.split(delim)).map(Double::parseDouble).toList();
    }
}
