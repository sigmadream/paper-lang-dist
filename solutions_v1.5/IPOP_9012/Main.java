import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String line = reader.readLine();
        if (line == null) return;
        StringTokenizer tokenizer = new StringTokenizer(line);
        while (!tokenizer.hasMoreTokens()) {
            line = reader.readLine();
            if (line == null) return;
            tokenizer = new StringTokenizer(line);
        }
        int t = Integer.parseInt(tokenizer.nextToken());
        PrintWriter writer = new PrintWriter(System.out);
        for (int i = 0; i < t; i++) {
            while (!tokenizer.hasMoreTokens()) {
                line = reader.readLine();
                if (line == null) break;
                tokenizer = new StringTokenizer(line);
            }
            if (!tokenizer.hasMoreTokens()) break;
            String s = tokenizer.nextToken();
            int bal = 0;
            boolean valid = true;
            for (int j = 0; j < s.length(); j++) {
                char c = s.charAt(j);
                if (c == '(') {
                    bal++;
                } else if (c == ')') {
                    bal--;
                }
                if (bal < 0) {
                    valid = false;
                    break;
                }
            }
            if (bal != 0) {
                valid = false;
            }
            writer.println(valid ? "YES" : "NO");
        }
        writer.flush();
    }
}
