package solutions;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import util.InputTransformer;

import static java.util.stream.Collectors.counting;
import static java.util.stream.Collectors.groupingBy;

public class Day01 extends Solution {

    public static void main(String[] args) {
        new Day01(true).solve();
    }

    public Day01(boolean isTest) {
        super(isTest);
    }

    List<Long> l1 = new ArrayList<>();
    List<Long> l2 = new ArrayList<>();

    @Override
    void processInput() {
        this.getFileContentsStream()
                .map(s -> InputTransformer.getInputStringAsListOfLongs(s, "   "))
                .forEach(this::addDigits);

        l1.sort(null);
        l2.sort(null);
    }

    @Override
    long part1() {
        long result = 0;
        for (int i = 0; i < l1.size(); i++) {
            result += Math.abs(l1.get(i) - l2.get(i));
        }

        return result;
    }

    long part2() {
        Map<Long, Long> counts = l2.stream().collect(groupingBy(l -> l, counting()));

        long result = 0;

        return l1.stream().reduce(0L, (a, b) -> a += b * counts.get(b));
    }

    private void addDigits(List<Long> digits) {
        l1.add(digits.get(0));
        l2.add(digits.get(1));
    }
}
