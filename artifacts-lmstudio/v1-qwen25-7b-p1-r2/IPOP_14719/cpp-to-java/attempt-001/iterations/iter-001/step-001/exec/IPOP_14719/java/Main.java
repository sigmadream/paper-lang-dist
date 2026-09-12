import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int h = scanner.nextInt();
        int w = scanner.nextInt();
        
        int[] a = new int[w];
        for (int i = 0; i < w; i++) {
            a[i] = scanner.nextInt();
        }
        
        int ans = 0;
        for (int i = 1; i < w - 1; i++) {
            int leftMax = 0, rightMax = 0;
            for (int j = 0; j <= i; j++) {
                leftMax = Math.max(leftMax, a[j]);
            }
            for (int j = i; j < w; j++) {
                rightMax = Math.max(rightMax, a[j]);
            }
            int bound = Math.min(leftMax, rightMax);
            if (bound > a[i]) {
                ans += bound - a[i];
            }
        }
        
        System.out.println(ans);
    }
}
