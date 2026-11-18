import java.io.*;
import java.util.*;
public class Main {
static final BufferedInputStream input = new BufferedInputStream(System.in);
static String next() throws Exception {StringBuilder word=new StringBuilder();int c;do{c=input.read();}while(c<=32 && c!=-1);while(c>32 && c!=-1){word.append((char)c);c=input.read();}return word.toString();}
static int nextInt() throws Exception {return Integer.parseInt(next());}
public static void main(String[] args) throws Exception {solve();}
static void solve() throws Exception {int n=nextInt(),m=nextInt();boolean[][] g=new boolean[n+1][n+1];for(int i=0;i<m;i++){int a=nextInt(),b=nextInt();g[a][b]=g[b][a]=true;}
boolean[] invited=g[1].clone();for(int i=1;i<=n;i++)if(g[1][i])for(int j=1;j<=n;j++)if(g[i][j])invited[j]=true;
int count=0;for(int i=2;i<=n;i++)if(invited[i])count++;System.out.println(count);}
}
