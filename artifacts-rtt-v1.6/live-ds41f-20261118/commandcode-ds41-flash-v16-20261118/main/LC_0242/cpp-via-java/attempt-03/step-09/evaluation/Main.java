import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String s = "";
        String t = "";

        String line = br.readLine();
        if (line != null) {
            s = line;
        }

        line = br.readLine();
        if (line != null) {
            t = line;
        }

        s = s.trim();
        t = t.trim();

        if (s.length() != t.length()) {
            System.out.println(0);
            return;
        }

        int[] counts = new int[26];

        for (int i = 0; i < s.length(); ++i) {
            ++counts[s.charAt(i) - 'a'];
            --counts[t.charAt(i) - 'a'];
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