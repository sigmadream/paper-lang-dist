import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s == null) return;
        int b = 0, e = s.length();
        while (e > 0 && (s.charAt(e-1)=='\r' || s.charAt(e-1)=='\n' || s.charAt(e-1)==' ' || s.charAt(e-1)=='\t')) e--;
        while (b < e && (s.charAt(b)==' ' || s.charAt(b)=='\t' || s.charAt(b)=='\r' || s.charAt(b)=='\n')) b++;
        String t = s.substring(b, e);
        boolean valid = true;
        for (int i = 0; i < t.length()/2; i++) {
            if (t.charAt(i) != t.charAt(t.length()-1-i)) { valid = false; break; }
        }
        System.out.println(valid ? 1 : 0);
    }
}