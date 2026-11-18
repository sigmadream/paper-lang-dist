import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String first = br.readLine();
        if (first == null) return;

        int t = Integer.parseInt(first.trim());
        StringBuilder output = new StringBuilder();

        for (int i = 0; i < t; i++) {
            String s = br.readLine();
            if (s == null) break;
            s = s.trim();

            int bal = 0;
            boolean valid = true;

            for (int j = 0; j < s.length(); j++) {
                char c = s.charAt(j);
                if (c == '(') {
                    bal++;
                } else {
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

            output.append(valid ? "YES\n" : "NO\n");
        }

        System.out.print(output);
    }
}