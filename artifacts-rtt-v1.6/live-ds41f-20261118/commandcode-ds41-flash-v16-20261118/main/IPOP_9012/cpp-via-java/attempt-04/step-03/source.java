import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String first = br.readLine();
        if (first == null) return;

        int idx = 0;
        int n = first.length();
        while (idx < n && Character.isWhitespace(first.charAt(idx))) idx++;

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
            String s = null;

            while (true) {
                String line = br.readLine();
                if (line == null) break;

                boolean empty = true;
                for (int j = 0; j < line.length(); j++) {
                    if (!Character.isWhitespace(line.charAt(j))) {
                        empty = false;
                        break;
                    }
                }

                if (!empty) {
                    s = line;
                    break;
                }
            }

            if (s == null) break;

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