import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());

        int count = 0;
        int value = 665;
        while (count < n) {
            ++value;
            if (String.valueOf(value).contains("666")) {
                ++count;
            }
        }

        System.out.println(value);
    }
}
