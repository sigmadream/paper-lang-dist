import java.io.*;

public class Main {
    static boolean isSpaceChar(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\f';
    }

    static String trimJava(String s) {
        int begin = 0;
        int end = s.length();
        while (begin < end && s.charAt(begin) <= ' ') ++begin;
        while (end > begin && s.charAt(end - 1) <= ' ') --end;
        return s.substring(begin, end);
    }

    static Integer parseJavaInt(String s) {
        if (s.isEmpty()) return null;
        int i = 0;
        boolean negative = false;
        char c0 = s.charAt(0);
        if (c0 == '+' || c0 == '-') {
            negative = (c0 == '-');
            ++i;
            if (i == s.length()) return null;
        }
        long value = 0;
        long limit = negative ? 2147483648L : 2147483647L;
        for (; i < s.length(); ++i) {
            char c = s.charAt(i);
            if (c < '0' || c > '9') return null;
            value = value * 10 + (c - '0');
            if (value > limit) return null;
        }
        return (int) (negative ? -value : value);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String firstLine = br.readLine();
        if (firstLine == null) return;

        firstLine = trimJava(firstLine);
        if (firstLine.isEmpty()) return;

        int pos = 0;
        while (pos < firstLine.length() && !isSpaceChar(firstLine.charAt(pos))) ++pos;

        String firstToken = firstLine.substring(0, pos);
        Integer nObj = parseJavaInt(firstToken);
        if (nObj == null) return;

        int n = nObj;
        if (n < 0) return;

        int[] a = new int[n];
        int count = 0;

        String line;
        while (count < n && (line = br.readLine()) != null) {
            int i = 0;
            while (i < line.length() && count < n) {
                while (i < line.length() && isSpaceChar(line.charAt(i))) ++i;
                if (i >= line.length()) break;

                int start = i;
                while (i < line.length() && !isSpaceChar(line.charAt(i))) ++i;

                String token = line.substring(start, i);
                Integer value = parseJavaInt(token);
                a[count++] = (value == null) ? 0 : value;
            }
        }

        while (count < n) {
            a[count++] = 0;
        }

        int write = 0;
        for (int read = 0; read < n; ++read) {
            if (a[read] != 0) {
                int tmp = a[write];
                a[write] = a[read];
                a[read] = tmp;
                ++write;
            }
        }

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; ++i) {
            if (i > 0) sb.append(' ');
            sb.append(a[i]);
        }
        sb.append('\n');
        System.out.print(sb);
    }
}