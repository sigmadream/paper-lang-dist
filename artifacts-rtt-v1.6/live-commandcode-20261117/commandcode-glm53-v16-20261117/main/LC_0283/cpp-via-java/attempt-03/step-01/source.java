import java.util.*;
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.parseNumbers();
        st.ordinaryChars('a','z'); // unused, keep defaults
        st.nextToken();
        int n = (int) st.nval;
        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            st.nextToken();
            a[i] = (long) st.nval;
        }
        int write = 0;
        for (int read = 0; read < n; read++) {
            if (a[read] != 0) {
                long t = a[write]; a[write] = a[read]; a[read] = t;
                write++;
            }
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            if (i > 0) sb.append(' ');
            sb.append(a[i]);
        }
        sb.append('\n');
        System.out.print(sb);
    }
}