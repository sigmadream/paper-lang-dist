import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n;
        try {
            n = Integer.parseInt(br.readLine().trim());
        } catch (Exception e) {
            return;
        }
        if (n < 1 || n > 20) return;

        int count = (1 << n) - 1;
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        bw.write(count + "\n");
        hanoi(n, 1, 2, 3, bw);
        bw.flush();
        bw.close();
    }

    private static void hanoi(int n, int from, int aux, int to, BufferedWriter bw) throws IOException {
        if (n == 1) {
            bw.write(from + " " + to + "\n");
            return;
        }
        hanoi(n - 1, from, to, aux, bw);
        bw.write(from + " " + to + "\n");
        hanoi(n - 1, aux, from, to, bw);
    }
}