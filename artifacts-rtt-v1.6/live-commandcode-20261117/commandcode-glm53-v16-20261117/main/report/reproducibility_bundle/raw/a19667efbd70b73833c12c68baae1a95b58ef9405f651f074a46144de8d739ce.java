import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        int start = 0, end = line.length();
        while (end > start && (line.charAt(end - 1) == '\n' || line.charAt(end - 1) == '\r'
                || line.charAt(end - 1) == ' ' || line.charAt(end - 1) == '\t')) end--;
        while (start < end && (line.charAt(start) == ' ' || line.charAt(start) == '\t')) start++;
        String s = line.substring(start, end);
        boolean valid = true;
        for (int i = 0; i < s.length() / 2; i++) {
            if (s.charAt(i) != s.charAt(s.length() - 1 - i)) { valid = false; break; }
        }
        System.out.println(valid ? 1 : 0);
    }
}