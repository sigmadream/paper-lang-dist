import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String first = br.readLine();
        if (first == null) return;
        int T = Integer.parseInt(first.trim());
        StringBuilder sb = new StringBuilder();
        for (int t = 0; t < T; t++) {
            String s = br.readLine();
            if (s == null) s = "";
            int bal = 0;
            boolean valid = true;
            for (int i = 0; i < s.length(); i++) {
                char c = s.charAt(i);
                if (c == '(') bal++;
                else bal--;
                if (bal < 0) {
                    valid = false;
                    break;
                }
            }
            if (bal != 0) valid = false;
            sb.append(valid ? "YES\n" : "NO\n");
        }
        System.out.print(sb);
    }
}