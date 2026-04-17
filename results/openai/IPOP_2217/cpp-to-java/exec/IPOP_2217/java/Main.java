import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        int n;
        try {
            n = fs.nextInt();
        } catch (Exception e) {
            return;
        }

        Integer[] ropes = new Integer[n];
        for (int i = 0; i < n; i++) {
            ropes[i] = fs.nextInt();
        }

        Arrays.sort(ropes, Collections.reverseOrder());

        long maxWeight = 0;
        for (int i = 0; i < n; i++) {
            long currentWeight = 1L * ropes[i] * (i + 1);
            if (currentWeight > maxWeight) {
                maxWeight = currentWeight;
            }
        }

        System.out.print(maxWeight + "\n");
    }

    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

        FastScanner(InputStream is) {
            in = is;
        }

        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }

        int nextInt() throws IOException {
            int c;
            do {
                c = read();
                if (c == -1) throw new EOFException();
            } while (c <= ' ');

            int sign = 1;
            if (c == '-') {
                sign = -1;
                c = read();
            }

            int val = 0;
            while (c > ' ') {
                val = val * 10 + (c - '0');
                c = read();
            }
            return val * sign;
        }
    }
}
