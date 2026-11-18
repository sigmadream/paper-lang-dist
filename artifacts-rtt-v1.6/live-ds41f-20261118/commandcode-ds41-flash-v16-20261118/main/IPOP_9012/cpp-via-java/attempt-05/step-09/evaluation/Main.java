import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    private static boolean isSpace(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\r' ||
               c == '\f' || c == '\v';
    }

    private static String trimStr(String s) {
        int b = 0;
        int e = s.length();

        while (b < e && isSpace(s.charAt(b))) {
            ++b;
        }
        while (e > b && isSpace(s.charAt(e - 1))) {
            --e;
        }

        return s.substring(b, e);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String first = br.readLine();
        if (first == null) {
            return;
        }

        int t = Integer.parseInt(trimStr(first));
        StringBuilder output = new StringBuilder();

        for (int i = 0; i < t; ++i) {
            String line = br.readLine();
            String s;
            if (line == null) {
                s = "";
            } else {
                s = trimStr(line);
            }

            int balance = 0;
            boolean valid = true;

            for (int j = 0; j < s.length(); ++j) {
                char c = s.charAt(j);
                if (c == '(') {
                    ++balance;
                } else {
                    --balance;
                }

                if (balance < 0) {
                    valid = false;
                    break;
                }
            }

            if (balance != 0) {
                valid = false;
            }

            output.append(valid ? "YES\n" : "NO\n");
        }

        System.out.print(output);
    }
}