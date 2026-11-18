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
        StringBuilder sb = new StringBuilder();
        sb.append(moves.size()).append('\n');
        for (int[] move : moves) {
            sb.append(move[0]).append(' ').append(move[1]).append('\n');
        }
        System.out.print(sb);
    }
}