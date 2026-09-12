import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        long m = scanner.nextLong();
        
        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextLong();
        }
        
        int ans = 0;
        long sum = 0;
        int end = 0;
        
        for (int start = 0; start < n; start++) {
            while (sum < m && end < n) {
                sum += a[end];
                end++;
            }
            if (sum == m) ans++;
            sum -= a[start];
        }
        
        System.out.println(ans);
    }
}
