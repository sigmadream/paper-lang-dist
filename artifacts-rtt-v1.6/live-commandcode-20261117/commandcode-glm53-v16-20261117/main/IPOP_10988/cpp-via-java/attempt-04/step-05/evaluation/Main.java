import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s == null) s = "";
        int start = 0;
        int end = s.length();
        while (end > start) {
            char c = s.charAt(end - 1);
            if (c == '\n' || c == '\r' || c == ' ' || c == '\t') {
                end--;
            } else {
                break;
            }
        }
        boolean valid = true;
        int len = end - start;
        for (int i = 0; i < len / 2; i++) {
            if (s.charAt(start + i) != s.charAt(end - 1 - i)) {
                valid = false;
                break;
            }
        }
        System.out.println(valid ? 1 : 0);
    }
}