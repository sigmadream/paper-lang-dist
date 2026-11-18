import java.util.*;
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int n = (int) st.nval;
        long[] arr = new long[n];
        for (int i = 0; i < n; i++) {
            st.nextToken();
            arr[i] = (long) st.nval;
        }
        int write = 0;
        for (int read = 0; read < n; read++) {
            if (arr[read] != 0) {
                long tmp = arr[write];
                arr[write] = arr[read];
                arr[read] = tmp;
                write++;
            }
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            if (i > 0) sb.append(' ');
            sb.append(arr[i]);
        }
        sb.append('\n');
        System.out.print(sb);
    }
}