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
        s = trim(s);
        t = trim(t);
        int[] counts = new int[26];
        for (char c : s.toCharArray()) counts[c - 'a']++;
        for (char c : t.toCharArray()) counts[c - 'a']--;
        boolean ok = true;
        for (int x : counts) if (x != 0) { ok = false; break; }
        System.out.println(ok ? 1 : 0);
    }

    private static String trim(String str) {
        int a = 0, b = str.length() - 1;
        while (a <= b && isWs(str.charAt(a))) a++;
        while (b >= a && isWs(str.charAt(b))) b--;
        return str.substring(a, b + 1);
    }

    private static boolean isWs(char c) {
        return c == ' ' || c == '\t' || c == '\r' || c == '\n';
    }
}