import java.io.*;
import java.util.*;
public class Main {
static final BufferedInputStream input = new BufferedInputStream(System.in);
static String next() throws Exception {StringBuilder word=new StringBuilder();int c;do{c=input.read();}while(c<=32 && c!=-1);while(c>32 && c!=-1){word.append((char)c);c=input.read();}return word.toString();}
static int nextInt() throws Exception {return Integer.parseInt(next());}
public static void main(String[] args) throws Exception {solve();}
static int mask;
static long search(int columns,int down,int up){if(columns==mask)return 1;int available=mask&~(columns|down|up);long count=0;
while(available!=0){int bit=available&-available;available-=bit;count+=search(columns|bit,(down|bit)<<1,(up|bit)>>>1);}return count;}
static void solve() throws Exception {int n=nextInt();mask=(1<<n)-1;long count=0;for(int c=0;c<n/2;c++){int b=1<<c;count+=2*search(b,b<<1,b>>>1);}if(n%2==1){int b=1<<(n/2);count+=search(b,b<<1,b>>>1);}System.out.println(count);}
}
