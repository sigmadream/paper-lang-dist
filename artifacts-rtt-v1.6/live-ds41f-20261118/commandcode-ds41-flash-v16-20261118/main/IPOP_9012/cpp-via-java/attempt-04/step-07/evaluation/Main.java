import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    private static boolean isWhitespace(char c) {
        return Character.isWhitespace(c);
    }

    private static boolean isEmptyOrWhitespace(String line) {
        for (int i = 0; i < line.length(); i++) {
            if (!isWhitespace(line.charAt(i))) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String first = br.readLine();
        if (first == null) return;

        int idx = 0;
        int n = first.length();

        while (idx < n && isWhitespace(first.charAt(idx))) idx++;

        int sign = 1;
        if (idx < n && (first.charAt(idx) == '+' || first.charAt(idx) == '-')) {
            if (first.charAt(idx) == '-') sign = -1;
            idx++;
        }

        int val = 0;
        while (idx < n && Character.isDigit(first.charAt(idx))) {
            val = val * 10 + (first.charAt(idx) - '0');
            idx++;
        }

        int t = sign * val;
        StringBuilder out = new StringBuilder();

        for (int i = 0; i < t; i++) {
            boolean found = false;
            String s = null;

            while (true) {
                String line = br.readLine();
                if (line == null) break;

                if (!isEmptyOrWhitespace(line)) {
                    s = line;
                    found = true;
                    break;
                }
            }

            if (!found) break;

            int balance = 0;
            boolean valid = true;

            for (int j = 0; j < s.length(); j++) {
                char c = s.charAt(j);

                if (c == '(') {
                    balance++;
                } else if (c == ')') {
                    balance--;
                }

                if (balance < 0) {
                    valid = false;
                    break;
                }
            }

            if (balance != 0) {
                valid = false;
            }

            out.append(valid ? "YES\n" : "NO\n");
        }

        System.out.print(out);
    }
}