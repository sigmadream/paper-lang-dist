import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.ordinaryChars(0, 255);
        st.wordChars('(', ')');
        st.whitespaceChars('\n', '\n');
        st.whitespaceChars('\r', '\r');
        st.whitespaceChars(' ', ' ');
        st.whitespaceChars('\t', '\t');
        st.eolIsSignificant(false);
        StringBuilder sb = new StringBuilder();
        if (st.nextToken() == StreamTokenizer.TT_EOF) return;
        int t = (int) st.nval;
        while (t-- > 0) {
            if (st.nextToken() == StreamTokenizer.TT_EOF) break;
            String s = st.sval;
            int bal = 0;
            boolean valid = true;
            for (char c : s.toCharArray()) {
                if (c == '(') bal++;
                else bal--;
                if (bal < 0) { valid = false; break; }
            }
            if (bal != 0) valid = false;
            sb.append(valid ? "YES" : "NO").append('\n');
        }
        System.out.print(sb);
    }
}