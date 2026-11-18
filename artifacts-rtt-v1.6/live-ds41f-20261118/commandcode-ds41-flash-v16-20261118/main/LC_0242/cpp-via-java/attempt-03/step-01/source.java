import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String s = br.readLine();
        String t = br.readLine();

        if (s == null) s = "";
        if (t == null) t = "";

        s = s.trim();
        t = t.trim();

        if (s.length() != t.length()) {
            System.out.println(0);
            return;
        }

        int[] counts = new int[26];

        for (int i = 0; i < s.length(); i++) {
            counts[s.charAt(i) - 'a']++;
            counts[t.charAt(i) - 'a']--;
        }

        for (int count : counts) {
            if (count != 0) {
                System.out.println(0);
                return;
            }
        }

        System.out.println(1);
    }
}