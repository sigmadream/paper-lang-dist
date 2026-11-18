import java.io.*;
import java.util.*;

public class Main {
    static class FastScanner {
        BufferedReader br;
        StringTokenizer st;

        FastScanner() {
            br = new BufferedReader(new InputStreamReader(System.in));
        }

        String next() {
            while (st == null || !st.hasMoreTokens()) {
                try {
                    String line = br.readLine();
                    if (line == null) return null;
                    st = new StringTokenizer(line);
                } catch (IOException e) {
                    return null;
                }
            }
            return st.nextToken();
        }
    }

    public static void main(String[] args) {
        FastScanner fs = new FastScanner();

        String ns = fs.next();
        if (ns == null) return;
        int n = Integer.parseInt(ns);

        String firstToken = fs.next();
        if (firstToken == null) return;

        long first = Long.parseLong(firstToken);
        long cur = first;
        long best = first;

        for (int i = 1; i < n; i++) {
            String token = fs.next();
            if (token == null) break;

            long x = Long.parseLong(token);
            cur = Math.max(x, cur + x);
            best = Math.max(best, cur);
        }

        System.out.println(best);
    }
}