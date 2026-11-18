import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;

        int t = Integer.parseInt(line.trim());
        StringBuilder output = new StringBuilder();

        while (t-- > 0) {
            String s = br.readLine();
            if (s == null) s = "";
            s = s.trim();

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

            output.append(valid ? "YES\n" : "NO\n");
        }

        System.out.print(output);
    }
}