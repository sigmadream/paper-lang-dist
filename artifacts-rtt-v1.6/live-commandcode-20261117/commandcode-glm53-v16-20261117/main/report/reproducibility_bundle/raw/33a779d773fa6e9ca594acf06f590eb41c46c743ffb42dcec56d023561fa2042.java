import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.nextToken();
        int t = (int) st.nval;
        StringBuilder sb = new StringBuilder();
        while (t-- > 0) {
            st.nextToken();
            String s = st.sval;
            int bal = 0;
            boolean valid = true;
            for (char c : s.toCharArray()) {
                if (c == '(') bal++;
                else bal--;
                if (bal < 0) {
                    valid = false;
                    break;
                }
            }
            if (bal != 0) valid = false;
            sb.append(valid ? "YES" : "NO").append('\n');
        }
        System.out.print(sb);
    }
}