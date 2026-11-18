import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int m = (int) st.nval;
        st.nextToken();
        int n = (int) st.nval;

        boolean[] isComposite = new boolean[n + 1];
        if (n >= 0) isComposite[0] = true;
        if (n >= 1) isComposite[1] = true;

        for (long i = 2; i * i <= n; i++) {
            if (!isComposite[(int) i]) {
                for (long j = i * i; j <= n; j += i) {
                    isComposite[(int) j] = true;
                }
            }
        }

        StringBuilder sb = new StringBuilder();
        for (int i = m; i <= n; i++) {
            if (!isComposite[i]) {
                sb.append(i).append('\n');
            }
        }
        System.out.print(sb);
    }
}