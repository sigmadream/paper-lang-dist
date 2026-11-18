import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();

        if (s == null) {
            return;
        }

        int left = 0;
        int right = s.length() - 1;

        while (left <= right && s.charAt(left) <= ' ') {
            ++left;
        }
        while (right >= left && s.charAt(right) <= ' ') {
            --right;
        }

        if (left > right) {
            return;
        }

        boolean valid = true;
        int n = right - left + 1;

        for (int i = 0; i < n / 2; ++i) {
            if (s.charAt(left + i) != s.charAt(right - i)) {
                valid = false;
                break;
            }
        }

        System.out.println(valid ? 1 : 0);
    }
}