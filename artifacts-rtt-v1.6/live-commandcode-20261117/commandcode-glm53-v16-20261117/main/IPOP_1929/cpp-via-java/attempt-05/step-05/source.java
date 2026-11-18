import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.ordinaryChars(0, 255);
        st.wordChars('0', '9');
        st.whitespaceChars(0, ' ');
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int m = Integer.parseInt(st.sval);
        st.nextToken();
        int n = Integer.parseInt(st.sval);

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