import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder out = new StringBuilder();
        String line = br.readLine();
        if (line == null) return;
        int t = Integer.parseInt(line.trim());
        for (int i = 0; i < t; i++) {
            String s = br.readLine();
            if (s == null) break;
            s = s.trim();
            int bal = 0;
            boolean valid = true;
            for (char c : s.toCharArray()) {
                if (c == '(') bal++;
                else bal--;
                if (bal < 0) { valid = false; break; }
            }
            if (bal != 0) valid = false;
            out.append(valid ? "YES" : "NO").append('\n');
        }
        System.out.print(out);
    }
}