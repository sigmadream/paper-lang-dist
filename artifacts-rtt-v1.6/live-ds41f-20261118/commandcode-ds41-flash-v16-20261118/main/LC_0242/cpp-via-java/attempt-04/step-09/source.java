import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String s = br.readLine();
        if (s == null) {
            return;
        }

        String t = br.readLine();
        if (t == null) {
            return;
        }

        s = trim(s);
        t = trim(t);

        if (s.isEmpty() || t.isEmpty()) {
            return;
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

    private static String trim(String str) {
        int begin = 0;
        while (begin < str.length() && isCppSpace(str.charAt(begin))) {
            begin++;
        }

        int end = str.length();
        while (end > begin && isCppSpace(str.charAt(end - 1))) {
            end--;
        }

        return str.substring(begin, end);
    }

    private static boolean isCppSpace(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\u000B' || c == '\f' || c == '\r';
    }
}