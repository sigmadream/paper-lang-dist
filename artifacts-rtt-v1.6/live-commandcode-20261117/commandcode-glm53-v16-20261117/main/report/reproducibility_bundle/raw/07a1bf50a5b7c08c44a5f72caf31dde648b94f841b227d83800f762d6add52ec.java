import java.util.*;
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.parseNumber();
        st.nextToken();
        int n = (int) st.nval;
        int[] counts = new int[n + 1];
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i <= n; i++) {
            if (i > 0) counts[i] = counts[i / 2] + (i % 2);
            if (i > 0) sb.append(' ');
            sb.append(counts[i]);
        }
        sb.append('\n');
        System.out.print(sb);
    }
}