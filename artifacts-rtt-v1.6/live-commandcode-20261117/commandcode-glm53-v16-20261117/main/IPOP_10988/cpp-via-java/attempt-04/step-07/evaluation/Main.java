import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s == null) s = "";
        int end = s.length();
        while (end > 0) {
            char c = s.charAt(end - 1);
            if (c == '\n' || c == '\r' || c == ' ' || c == '\t') end--;
            else break;
        }
        boolean valid = true;
        int len = end;
        for (int i = 0; i < len / 2; i++) {
            if (s.charAt(i) != s.charAt(end - 1 - i)) { valid = false; break; }
        }
        System.out.println(valid ? 1 : 0);
    }
}