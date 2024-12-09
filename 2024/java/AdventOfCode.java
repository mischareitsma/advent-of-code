import util.InputReader;
public class AdventOfCode {

    int day;
    int part;
    int subPart;
    boolean isTest;

    public static void main(String[] args) {
        AdventOfCode aoc = new AdventOfCode();
        aoc.processArgs(args);
    }

    private void processArgs(String[] args) {
        boolean foundDay = false;
        boolean foundPart = false;
        for (String arg: args) {
            if (arg.equals("-t")) {
                isTest=true;
            }
            if (arg.startsWith("-d")) {
                day = Integer.parseInt(arg.substring(2));
                foundDay = true;
            }
            if (arg.startsWith("-p")) {
                part = Integer.parseInt(arg.substring(2));
                foundPart = true;
            }
            if (arg.startsWith("-s")) {
                subPart = Integer.parseInt(arg.substring(2));
            }
        }

        if (!foundDay) throw new RuntimeException("Missing required argument -d");
        if (!foundPart) throw new RuntimeException("Missing required argument -p");
    }
}
