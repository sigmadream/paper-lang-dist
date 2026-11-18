import java.io.*;
import java.util.*;
public class Main {
static final BufferedInputStream input = new BufferedInputStream(System.in);
static String next() throws Exception {StringBuilder word=new StringBuilder();int c;do{c=input.read();}while(c<=32 && c!=-1);while(c>32 && c!=-1){word.append((char)c);c=input.read();}return word.toString();}
static int nextInt() throws Exception {return Integer.parseInt(next());}
public static void main(String[] args) throws Exception {solve();}
static void solve() throws Exception {int n=nextInt();int[] a=new int[n+1],dp=new int[n+1];for(int i=1;i<=n;i++)a[i]=nextInt();
if(n>=1)dp[1]=a[1];if(n>=2)dp[2]=a[1]+a[2];for(int i=3;i<=n;i++)dp[i]=Math.max(dp[i-2],dp[i-3]+a[i-1])+a[i];System.out.println(dp[n]);}
}
