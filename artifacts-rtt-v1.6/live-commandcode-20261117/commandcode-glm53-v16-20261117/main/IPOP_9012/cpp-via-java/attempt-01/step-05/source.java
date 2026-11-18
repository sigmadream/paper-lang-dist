import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        int t = Integer.parseInt(line.trim());
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < t; i++) {
            String s = br.readLine();
            if (s == null) break;
            s = s.trim();
            boolean valid = true;
            int bal = 0;
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