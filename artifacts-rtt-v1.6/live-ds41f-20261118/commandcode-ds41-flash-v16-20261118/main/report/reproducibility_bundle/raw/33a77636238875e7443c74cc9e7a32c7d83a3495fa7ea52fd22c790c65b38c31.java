import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    private static String trim(String str) {
        int start = 0;
        int end = str.length();

        while (start < end && str.charAt(start) <= ' ') {
            ++start;
        }

        while (end > start && str.charAt(end - 1) <= ' ') {
            --end;
        }

        return str.substring(start, end);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String s = br.readLine();
        if (s == null) {
            s = "";
        }

        String t = br.readLine();
        if (t == null) {
            t = "";
        }

        s = trim(s);
        t = trim(t);

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