import java.io.*;
import java.util.*;

public class Main {
    static void hanoi(int n, int start, int mid, int end, List<int[]> moves) {
        if (n == 1) {
            moves.add(new int[]{start, end});
            return;
        }
        hanoi(n - 1, start, end, mid, moves);
        moves.add(new int[]{start, end});
        hanoi(n - 1, mid, start, end, moves);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null || line.trim().isEmpty()) {
            return;
        }
        int n = Integer.parseInt(line.trim());
        List<int[]> moves = new ArrayList<>();
        hanoi(n, 1, 2, 3, moves);
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        bw.write(String.valueOf(moves.size()));
        bw.newLine();
        for (int[] move : moves) {
            bw.write(move[0] + " " + move[1]);
            bw.newLine();
        }
        bw.flush();
    }
}