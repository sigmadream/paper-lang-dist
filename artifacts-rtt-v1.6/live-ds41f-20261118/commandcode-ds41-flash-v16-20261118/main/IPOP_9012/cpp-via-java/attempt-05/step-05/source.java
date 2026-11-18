import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String first = br.readLine();
        if (first == null) return;

        int t = Integer.parseInt(first.trim());
        StringBuilder output = new StringBuilder();

        for (int i = 0; i < t; i++) {
            String s = br.readLine();
            if (s == null) s = "";
            s = s.trim();

            int balance = 0;
            boolean valid = true;

            for (int j = 0; j < s.length(); j++) {
                char c = s.charAt(j);
                if (c == '(') {
                    balance++;
                } else {
                    balance--;
                }

                if (balance < 0) {
                    valid = false;
                    break;
                }
            }

            if (balance != 0) valid = false;

            output.append(valid ? "YES\n" : "NO\n");
        }

        System.out.print(output);
    }
}