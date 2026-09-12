import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt();
        }
        
        Arrays.sort(a);
        List<Integer> sortedA = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if (i == 0 || a[i] != a[i - 1]) {
                sortedA.add(a[i]);
            }
        }
        
        for (int i = 0; i < n; i++) {
            int compressed = sortedA.indexOf(a[i]);
            System.out.print(compressed + " ");
        }
        System.out.println();
    }
}
