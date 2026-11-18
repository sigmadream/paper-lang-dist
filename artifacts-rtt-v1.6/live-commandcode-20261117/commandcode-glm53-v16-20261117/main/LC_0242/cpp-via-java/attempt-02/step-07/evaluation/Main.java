import java.io.*;

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
        int a = 0, b = str.length();
        while (a < b && isSpace(str.charAt(a))) a++;
        while (b > a && isSpace(str.charAt(b - 1))) b--;
        return str.substring(a, b);
    }

    private static boolean isSpace(char c) {
        return c == ' ' || c == '\t' || c == '\r' || c == '\n';
    }
}