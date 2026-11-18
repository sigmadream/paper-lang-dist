import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String first = br.readLine();
        if (first == null) {
            return;
        }

        int t = Integer.parseInt(first.trim());
        StringBuilder output = new StringBuilder();

        for (int i = 0; i < t; i++) {
            String s = br.readLine();
            if (s == null) {
                break;
            }

            int start = 0;
            int end = s.length() - 1;
            while (start <= end && (s.charAt(start) == ' ' || s.charAt(start) == '\t' ||
                    s.charAt(start) == '\r' || s.charAt(start) == '\n')) {
                start++;
            }
            while (end >= start && (s.charAt(end) == ' ' || s.charAt(end) == '\t' ||
                    s.charAt(end) == '\r' || s.charAt(end) == '\n')) {
                end--;
            }
            s = start <= end ? s.substring(start, end + 1) : "";

            int bal = 0;
            boolean valid = true;

            for (int j = 0; j < s.length(); j++) {
                if (s.charAt(j) == '(') {
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