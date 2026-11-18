import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = readLine(br);
        String t = readLine(br);

        int[] counts = new int[26];
        for (int i = 0; i < s.length(); i++) {
            counts[s.charAt(i) - 'a']++;
        }
        for (int i = 0; i < t.length(); i++) {
            counts[t.charAt(i) - 'a']--;
        }

        boolean valid = true;
        for (int c : counts) {
            if (c != 0) {
                valid = false;
                break;
            }
        }

        System.out.println(valid ? 1 : 0);
    }

    private static String readLine(BufferedReader br) throws IOException {
        String line = br.readLine();
        if (line == null) line = "";
        if (line.endsWith("\r")) line = line.substring(0, line.length() - 1);
        return line;
    }
}