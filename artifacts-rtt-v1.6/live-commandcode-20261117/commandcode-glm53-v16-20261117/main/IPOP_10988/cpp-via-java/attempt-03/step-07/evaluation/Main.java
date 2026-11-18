import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s == null) s = "";
        s = s.replaceAll("^[ \\t\\r\\n]+", "").replaceAll("[ \\t\\r\\n]+$", "");
        int len = s.length();
        boolean valid = true;
        for (int i = 0; i < len / 2; i++) {
            if (s.charAt(i) != s.charAt(len - 1 - i)) { valid = false; break; }
        }
        System.out.println(valid ? 1 : 0);
    }
}