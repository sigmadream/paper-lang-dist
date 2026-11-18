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
            while (!s.isEmpty() && (s.charAt(s.length()-1)=='\r' || s.charAt(s.length()-1)==' ' || s.charAt(s.length()-1)=='\n'))
                s = s.substring(0, s.length()-1);
            int b = 0;
            while (b < s.length() && (s.charAt(b)==' ' || s.charAt(b)=='\t')) b++;
            s = s.substring(b);
            boolean valid = true;
            int bal = 0;
            for (int j = 0; j < s.length(); j++) {
                char c = s.charAt(j);
                if (c == '(') bal++;
                else bal--;
                if (bal < 0) { valid = false; break; }
            }
            if (bal != 0) valid = false;
            out.append(valid ? "YES\n" : "NO\n");
        }
        System.out.print(out);
    }
}