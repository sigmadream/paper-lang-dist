import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        StreamTokenizer st = new StreamTokenizer(new BufferedReader(new InputStreamReader(System.in)));
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int n = (int) st.nval;
        long cur = 0, best = Long.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            st.nextToken();
            long x = (long) st.nval;
            if (i == 0) {
                cur = x;
                best = x;
            } else {
                cur = Math.max(x, cur + x);
                best = Math.max(best, cur);
            }
        }
        StringBuilder sb = new StringBuilder();
        sb.append(best).append('\n');
        System.out.print(sb);
    }
}