import util.InputTransformer;

public class Test {
    public static void main(String[] args) {
        for (Long l: InputTransformer.getInputStringAsListOfLongs("1, 2, 3", ", ")) {
            System.out.println(l);
        }

        InputTransformer.getInputStringAsListOfDoubles("1;3.14;2.17", ";").forEach(System.out::println);
    }
}
