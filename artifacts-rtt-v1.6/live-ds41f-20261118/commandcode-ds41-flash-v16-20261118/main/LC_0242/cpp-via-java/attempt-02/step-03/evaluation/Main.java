import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String s = br.readLine();
        String t = br.readLine();

        if (s == null) s = "";
        if (t == null) t = "";

        if (!s.isEmpty() && s.charAt(s.length() - 1) == '\r') {
            s = s.substring(0, s.length() - 1);
        }
        if (!t.isEmpty() && t.charAt(t.length() - 1) == '\r') {
            t = t.substring(0, t.length() - 1);
        }

        int[] counts = new int[26];

        for (int i = 0; i < s.length(); i++) {
            counts[s.charAt(i) - 'a']++;
        }
        for (int i = 0; i < t.length(); i++) {
            counts[t.charAt(i) - 'a']--;
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