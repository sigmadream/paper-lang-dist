import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s != null) {
            s = s.trim();
        }
        if (s == null || s.isEmpty()) {
            return;
        }

        boolean valid = true;
        for (int i = 0; i < s.length() / 2; i++) {
            if (s.charAt(i) != s.charAt(s.length() - 1 - i)) {
                valid = false;
                break;
            }
        }
        System.out.println(valid ? 1 : 0);
    }
}