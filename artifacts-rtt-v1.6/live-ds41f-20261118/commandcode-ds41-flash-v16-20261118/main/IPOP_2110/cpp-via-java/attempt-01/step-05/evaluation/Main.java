import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String[] first = br.readLine().trim().split("\\s+");
        int n = Integer.parseInt(first[0]);
        int c = Integer.parseInt(first[1]);

        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = Integer.parseInt(br.readLine().trim());
        }

        Arrays.sort(a);

        int left = 1;
        int right = a[n - 1] - a[0];
        int ans = 0;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            int count = 1;
            int prev = a[0];

            for (int i = 1; i < n; i++) {
                if (a[i] - prev >= mid) {
                    count++;
                    prev = a[i];
                }
            }

            if (count >= c) {
                ans = mid;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        System.out.println(ans);
    }
}