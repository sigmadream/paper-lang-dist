import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int n = Integer.parseInt(st.nextToken());
        int c = Integer.parseInt(st.nextToken());

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
                    if (count >= c) {
                        break;
                    }
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