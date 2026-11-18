import java.io.*;
import java.util.*;

public class Main {
    static String trim(String s) {
        int start = 0, end = s.length();
        while (start < end && s.charAt(start) <= ' ') start++;
        while (end > start && s.charAt(end - 1) <= ' ') end--;
        return s.substring(start, end);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String first = br.readLine();
        if (first == null) return;

        int t = Integer.parseInt(trim(first));
        StringBuilder output = new StringBuilder();

        for (int i = 0; i < t; i++) {
            String s = br.readLine();
            if (s == null) s = "";
            s = trim(s);

            int bal = 0;
            boolean valid = true;

            for (int j = 0; j < s.length(); j++) {
                char c = s.charAt(j);
                if (c == '(') bal++;
                else bal--;

                if (bal < 0) {
                    valid = false;
                    break;
                }
            }

            if (bal != 0) valid = false;
            output.append(valid ? "YES\n" : "NO\n");
        }

        System.out.print(output);
    }
}