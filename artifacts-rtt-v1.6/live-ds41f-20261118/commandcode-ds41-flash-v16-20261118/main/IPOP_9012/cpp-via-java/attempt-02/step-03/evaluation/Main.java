import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String first = br.readLine();
        if (first == null) return;
        int t = Integer.parseInt(first.trim());
        StringBuilder out = new StringBuilder();
        while (t-- > 0) {
            String s = br.readLine();
            int bal = 0;
            boolean valid = true;
            for (int i = 0; i < s.length(); i++) {
                if (s.charAt(i) == '(') bal++;
                else bal--;
                if (bal < 0) {
                    valid = false;
                    break;
                }
            }
            if (bal != 0) valid = false;
            out.append(valid ? "YES\n" : "NO\n");
        }
        System.out.print(out);
    }
}