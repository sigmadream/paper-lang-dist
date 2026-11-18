import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.ordinaryChars(0, 256);
        st.wordChars(33, 126);
        st.whitespaceChars(0, ' ');
        st.parseNumbers();
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int n = (int) st.nval;
        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            st.nextToken();
            a[i] = (long) st.nval;
        }
        int write = 0;
        for (int read = 0; read < n; read++) {
            if (a[read] != 0) {
                long tmp = a[write];
                a[write] = a[read];
                a[read] = tmp;
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