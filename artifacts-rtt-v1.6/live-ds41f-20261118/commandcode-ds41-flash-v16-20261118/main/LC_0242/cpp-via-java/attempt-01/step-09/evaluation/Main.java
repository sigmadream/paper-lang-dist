import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String s = reader.readLine();
        String t = reader.readLine();

        if (s == null) s = "";
        if (t == null) t = "";

        int[] counts = new int[26];

        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= 'a' && c <= 'z') {
                counts[c - 'a']++;
            }
        }

        for (int i = 0; i < t.length(); i++) {
            char c = t.charAt(i);
            if (c >= 'a' && c <= 'z') {
                counts[c - 'a']--;
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