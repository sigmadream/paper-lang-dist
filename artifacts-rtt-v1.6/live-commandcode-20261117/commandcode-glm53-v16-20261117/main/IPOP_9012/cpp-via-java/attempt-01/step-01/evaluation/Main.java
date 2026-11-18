import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer in = new StreamTokenizer(br);
        in.ordinaryChars(33, 126);
        in.wordChars(33, 126);
        in.whitespaceChars(0, 32);
        if (in.nextToken() == StreamTokenizer.TT_EOF) return;
        int t = Integer.parseInt(in.sval);
        StringBuilder sb = new StringBuilder();
        while (t-- > 0) {
            if (in.nextToken() == StreamTokenizer.TT_EOF) break;
            String s = in.sval;
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