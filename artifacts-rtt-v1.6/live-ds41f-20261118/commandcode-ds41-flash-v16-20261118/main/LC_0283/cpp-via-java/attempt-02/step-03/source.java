import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String firstLine = br.readLine();
        if (firstLine == null) return;

        StringTokenizer st = new StringTokenizer(firstLine);
        if (!st.hasMoreTokens()) return;
        int n = Integer.parseInt(st.nextToken());

        int[] a = new int[n];
        StringBuilder sb = new StringBuilder();
        while (br.ready()) {
            sb.append(br.readLine()).append(' ');
        }

        st = new StringTokenizer(sb.toString());
        for (int i = 0; i < n; ++i) {
            if (st.hasMoreTokens()) {
                a[i] = Integer.parseInt(st.nextToken());
            }
        }

        int write = 0;
        for (int read = 0; read < n; ++read) {
            if (a[read] != 0) {
                int temp = a[write];
                a[write] = a[read];
                a[read] = temp;
                ++write;
            }
        }

        StringBuilder out = new StringBuilder();
        for (int i = 0; i < n; ++i) {
            if (i > 0) out.append(' ');
            out.append(a[i]);
        }
        out.append('\n');
        System.out.print(out);
    }
}