import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new StringBuilderReader(""));
        StreamTokenizer in = new StreamTokenizer(new BufferedReader(new InputStreamReader(System.in)));
        int n = (int) nextLong(in);
        long[] a = new long[n];
        for (int i = 0; i < n; i++) a[i] = nextLong(in);
        long cur = a[0], best = a[0];
        for (int i = 1; i < n; i++) {
            cur = Math.max(a[i], cur + a[i]);
            best = Math.max(best, cur);
        }
        System.out.println(best);
    }

    static long nextLong(StreamTokenizer in) throws IOException {
        in.nextToken();
        return (long) in.nval;
    }
}