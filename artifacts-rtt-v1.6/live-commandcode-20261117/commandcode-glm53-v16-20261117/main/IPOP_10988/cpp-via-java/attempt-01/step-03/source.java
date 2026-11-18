import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s == null) return;
        while (!s.isEmpty() && (s.charAt(s.length()-1)=='\n' || s.charAt(s.length()-1)=='\r'
                || s.charAt(s.length()-1)==' ' || s.charAt(s.length()-1)=='\t')) {
            s = s.substring(0, s.length()-1);
        }
        int b = 0;
        while (b < s.length() && (s.charAt(b)==' ' || s.charAt(b)=='\t')) b++;
        s = s.substring(b);
        boolean valid = true;
        for (int i = 0; i < s.length()/2; i++) {
            if (s.charAt(i) != s.charAt(s.length()-1-i)) { valid = false; break; }
        }
        System.out.println(valid ? 1 : 0);
    }
}