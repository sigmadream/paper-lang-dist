import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) {
            return;
        }

        int begin = 0;
        int end = line.length();

        while (begin < end && line.charAt(begin) <= ' ') {
            ++begin;
        }
        while (end > begin && line.charAt(end - 1) <= ' ') {
            --end;
        }

        if (begin >= end) {
            return;
        }

        boolean valid = true;
        for (int i = begin; i < begin + (end - begin) / 2; ++i) {
            if (line.charAt(i) != line.charAt(end - 1 - (i - begin))) {
                valid = false;
                break;
            }
        }

        System.out.println(valid ? 1 : 0);
    }
}