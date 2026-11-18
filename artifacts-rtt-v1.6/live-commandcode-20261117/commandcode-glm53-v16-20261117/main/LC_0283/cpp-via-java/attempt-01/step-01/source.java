import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.parseNumbers();
        st.ordinaryChars(Integer.MIN_VALUE, Integer.MAX_VALUE == Integer.MAX_VALUE ? 0 : 0);
        StreamTokenizer in = new StreamTokenizer(br);
        in.parseNumbers();
        int n = (int) readLong(in);
        long[] a = new long[n];
        for (int i = 0; i < n; i++) a[i] = readLong(in);
        int write = 0;
        for (int read = 0; read < n; read++) {
            if (a[read] != 0) {
                long t = a[write];
                a[write] = a[read];
                a[read] = t;
                write++;
            }
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            if (i > 0) sb.append(' ');
            sb.append(a[i]);
        }
        System.out.println(sb);
    }

    static long readLong(StreamTokenizer in) throws IOException {
        int t = in.nextToken();
        if (t == StreamTokenizer.TT_NUMBER) return (long) in.nval;
        throw new IOException("expected number");
    }
}