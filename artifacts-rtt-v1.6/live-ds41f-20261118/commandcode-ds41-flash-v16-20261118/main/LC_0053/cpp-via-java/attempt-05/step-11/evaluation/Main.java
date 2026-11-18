import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer in = new StreamTokenizer(br);
        in.nextToken();
        if (in.ttype == StreamTokenizer.TT_EOF) return;
        long n = (long) in.nval;
        if (n <= 0) return;

        if (in.nextToken() == StreamTokenizer.TT_EOF) return;
        long x = (long) in.nval;
        long cur = x;
        long best = x;

        for (long i = 1; i < n; ++i) {
            if (in.nextToken() == StreamTokenizer.TT_EOF) break;
            x = (long) in.nval;
            cur = Math.max(x, cur + x);
            best = Math.max(best, cur);
        }

        System.out.println(best);
    }
}