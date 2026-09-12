import java.util.Arrays;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] ropes = new int[n];
        for (int i = 0; i < n; i++) {
            ropes[i] = scanner.nextInt();
        }
        Arrays.sort(ropes);
        long max_weight = 0;
        for (int i = 0; i < n; i++) {
            long current_weight = 1L * ropes[i] * (i + 1);
            if (current_weight > max_weight) {
                max_weight = current_weight;
            }
        }
        System.out.println(max_weight);
    }
}
