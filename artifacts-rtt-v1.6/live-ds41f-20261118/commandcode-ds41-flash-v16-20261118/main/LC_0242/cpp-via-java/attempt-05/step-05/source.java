import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String s = readLine(br);
        String t = readLine(br);

        if (s == null || t == null) {
            System.out.println(0);
            return;
        }
        if (s.length() != t.length()) {
            System.out.println(0);
            return;
        }

        int[] counts = new int[26];
        for (int i = 0; i < s.length(); i++) {
            counts[s.charAt(i) - 'a']++;
            counts[t.charAt(i) - 'a']--;
        }
        for (int c : counts) {
            if (c != 0) {
                System.out.println(0);
                return;
            }
        }
        System.out.println(1);
    }

    private static String readLine(BufferedReader br) throws IOException {
        String line = br.readLine();
        if (line == null) return null;
        if (!line.isEmpty() && line.charAt(line.length() - 1) == '\r') {
            line = line.substring(0, line.length() - 1);
        }
        return line;
    }
}