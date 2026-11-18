import java.io.*;
import java.util.*;

public class Main {
    static int gcdInt(int a, int b) {
        while (b != 0) {
            int r = a % b;
            a = b;
            b = r;
        }
        return a;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st = new StringTokenizer(br.readLine());
        int a = Integer.parseInt(st.nextToken());
        int b = Integer.parseInt(st.nextToken());
        int g = gcdInt(a, b);
        sb.append(g).append('\n');
        sb.append((long) (a / g) * b).append('\n');
        System.out.print(sb);
    }
}