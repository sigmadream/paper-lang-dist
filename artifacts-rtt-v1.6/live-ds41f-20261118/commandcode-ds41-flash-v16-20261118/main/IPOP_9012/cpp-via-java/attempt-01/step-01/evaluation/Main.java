import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String first = br.readLine();
        if (first == null) return;

        int t = Integer.parseInt(first.trim());
        StringBuilder sb = new StringBuilder();

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

            sb.append(valid ? "YES" : "NO").append('\n');
        }

        System.out.print(sb);
    }
}