import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        String t = br.readLine();

        int[] counts = new int[26];

        if (s != null) {
            for (int i = 0; i < s.length(); i++) {
                char c = s.charAt(i);
                if (c >= 'a' && c <= 'z') {
                    counts[c - 'a']++;
                }
            }
        }

        if (t != null) {
            for (int i = 0; i < t.length(); i++) {
                char c = t.charAt(i);
                if (c >= 'a' && c <= 'z') {
                    counts[c - 'a']--;
                }
            }
        }

        boolean valid = true;
        for (int count : counts) {
            if (count != 0) {
                valid = false;
                break;
            }
        }

        System.out.println(valid ? 1 : 0);
    }
}