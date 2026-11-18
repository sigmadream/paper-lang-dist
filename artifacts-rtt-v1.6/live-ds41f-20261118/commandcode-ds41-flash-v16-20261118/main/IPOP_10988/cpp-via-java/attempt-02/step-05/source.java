import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s == null) {
            return;
        }
        s = s.trim();
        if (s.isEmpty()) {
            return;
        }

        boolean valid = true;
        int n = s.length();
        for (int i = 0; i < n / 2; i++) {
            if (s.charAt(i) != s.charAt(n - 1 - i)) {
                valid = false;
                break;
            }
        }

        System.out.println(valid ? 1 : 0);
    }
}