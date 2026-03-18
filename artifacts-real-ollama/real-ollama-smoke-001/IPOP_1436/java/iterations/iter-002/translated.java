import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        
        int count = 0;
        int value = 665;
        while (count < n) {
            ++value;
            if (String.valueOf(value).contains("666")) {
                ++count;
            }
        }

        System.out.println(value);
    }
}
