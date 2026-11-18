import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.parseNumbers();

        st.nextToken();
        int n = (int) st.nval;
        st.nextToken();
        int c = (int) st.nval;

        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            st.nextToken();
            a[i] = (int) st.nval;
        }

        Arrays.sort(a);

        long left = 1;
        long right = (long) a[n - 1] - a[0];
        long ans = 0;

        while (left <= right) {
            long mid = left + (right - left) / 2;
            int count = 1;
            int prev = a[0];

            for (int i = 1; i < n; i++) {
                if ((long) a[i] - prev >= mid) {
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