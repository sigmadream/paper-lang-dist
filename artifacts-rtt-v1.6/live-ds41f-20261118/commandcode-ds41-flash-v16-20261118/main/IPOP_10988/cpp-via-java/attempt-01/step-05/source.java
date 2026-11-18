import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) {
            return;
        }

        int begin = 0;
        int end = line.length();
        while (begin < end && line.charAt(begin) <= ' ') {
            begin++;
        }
        while (end > begin && line.charAt(end - 1) <= ' ') {
            end--;
        }

        String s = line.substring(begin, end);
        if (s.isEmpty()) {
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