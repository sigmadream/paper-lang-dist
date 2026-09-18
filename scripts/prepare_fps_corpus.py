"""Prepare the prospectively selected 15-problem, three-language corpus.

No model outputs are consulted. Existing statements, C++ and all 13 held-out
fixtures are copied unchanged; added references are independently implemented.
"""
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'data/fps-v1'
GROUPS = {
    'numeric': ['IPOP_2609', 'IPOP_1929', 'LC_0338'],
    'strings': ['IPOP_10988', 'IPOP_9012', 'LC_0242'],
    'lists': ['LC_0217', 'LC_0283', 'LC_0912'],
    'dynamic_programming': ['IPOP_2579', 'LC_0062', 'LC_0053'],
    'search_relations': ['LC_0547', 'LC_0704', 'IPOP_5567'],
}
PILOT = ['IPOP_2609', 'IPOP_9012', 'LC_0547']

HS = {
'IPOP_2609': '''euclid a 0 = a
euclid a b = euclid b (a `mod` b)
main = do
  [a,b] <- fmap (map read . words) getContents :: IO [Integer]
  let g = euclid a b
  print g
  print ((a `div` g) * b)
''',
'IPOP_1929': '''prime n = n >= 2 && trial 2
  where
    trial d | d*d > n = True
            | n `mod` d == 0 = False
            | otherwise = trial (d+1)
main = do
  [lo,hi] <- fmap (map read . words) getContents :: IO [Int]
  mapM_ print (filter prime [lo..hi])
''',
'LC_0338': '''ones 0 = 0
ones n = n `mod` 2 + ones (n `div` 2)
main = do
  n <- fmap read getContents :: IO Int
  putStrLn (unwords (map (show . ones) [0..n]))
''',
'IPOP_10988': '''palindrome [] = True
palindrome [_] = True
palindrome xs = head xs == last xs && palindrome (init (tail xs))
main = do
  s <- fmap (head . words) getContents
  print (if palindrome s then (1::Int) else 0)
''',
'IPOP_9012': '''balanced [] depth = depth == 0
balanced (c:cs) depth
  | depth < 0 = False
  | c == '(' = balanced cs (depth+1)
  | otherwise = balanced cs (depth-1)
main = do
  input <- fmap words getContents
  let n = read (head input) :: Int
  mapM_ (putStrLn . (\\s -> if balanced s (0::Int) then "YES" else "NO")) (take n (tail input))
''',
'LC_0242': '''import Data.List (sort)
frequencies [] = []
frequencies (x:xs) = let (same,rest) = span (==x) xs
                      in (x,1+length same) : frequencies rest
main = do
  [a,b] <- fmap words getContents
  print (if frequencies (sort a) == frequencies (sort b) then (1::Int) else 0)
''',
'LC_0217': '''import Data.List (sort)
duplicate (a:b:xs) = a == b || duplicate (b:xs)
duplicate _ = False
main = do
  values <- fmap (map read . words) getContents :: IO [Integer]
  let xs = take (fromInteger (head values)) (tail values)
  print (if duplicate (sort xs) then (1::Int) else 0)
''',
'LC_0283': '''main = do
  values <- fmap (map read . words) getContents :: IO [Integer]
  let n = fromInteger (head values)
      xs = take n (tail values)
      nonzero = filter (/=0) xs
      answer = nonzero ++ replicate (n-length nonzero) 0
  putStrLn (unwords (map show answer))
''',
'LC_0912': '''merge [] ys = ys
merge xs [] = xs
merge (x:xs) (y:ys)
  | x <= y = x : merge xs (y:ys)
  | otherwise = y : merge (x:xs) ys
mergesort [] = []
mergesort [x] = [x]
mergesort xs = let (a,b) = splitAt (length xs `div` 2) xs
               in merge (mergesort a) (mergesort b)
main = do
  values <- fmap (map read . words) getContents :: IO [Int]
  putStrLn (unwords (map show (mergesort (take (head values) (tail values)))))
''',
'IPOP_2579': '''import Data.Array
main = do
  values <- fmap (map read . words) getContents :: IO [Int]
  let n = head values
      score = listArray (1,n) (tail values)
      best = listArray (0,n) [value i | i <- [0..n]]
      value 0 = 0
      value 1 = score!1
      value 2 = score!1 + score!2
      value i = max (best!(i-2)) (best!(i-3) + score!(i-1)) + score!i
  print (best!n)
''',
'LC_0062': '''import Data.Array
main = do
  [m,n] <- fmap (map read . words) getContents :: IO [Int]
  let table = array ((1,1),(m,n)) [((i,j), value i j) | i <- [1..m], j <- [1..n]]
      value 1 _ = 1 :: Integer
      value _ 1 = 1
      value i j = table!(i-1,j) + table!(i,j-1)
  print (table!(m,n))
''',
'LC_0053': '''import Data.List (foldl')
step (ending,best) x = let next = max x (ending+x)
                       in (next,max best next)
main = do
  values <- fmap (map read . words) getContents :: IO [Integer]
  let xs = take (fromInteger (head values)) (tail values)
  print (snd (foldl' step (head xs,head xs) (tail xs)))
''',
'LC_0547': '''import Data.Array
import qualified Data.IntSet as S
visit graph [] seen = seen
visit graph (v:todo) seen
  | S.member v seen = visit graph todo seen
  | otherwise = visit graph (graph!v ++ todo) (S.insert v seen)
components graph [] seen = 0
components graph (v:vs) seen
  | S.member v seen = components graph vs seen
  | otherwise = 1 + components graph vs (visit graph [v] seen)
main = do
  values <- fmap (map read . words) getContents :: IO [Int]
  let n = head values
      matrix = listArray ((0,0),(n-1,n-1)) (tail values)
      graph = listArray (0,n-1) [[j | j <- [0..n-1], matrix!(i,j)==1] | i <- [0..n-1]]
  print (components graph [0..n-1] S.empty :: Int)
''',
'LC_0704': '''import Data.Array
search array target lo hi
  | lo > hi = -1
  | array!mid == target = mid
  | array!mid < target = search array target (mid+1) hi
  | otherwise = search array target lo (mid-1)
  where mid = (lo+hi) `div` 2
main = do
  (n:target:xs) <- fmap (map read . words) getContents :: IO [Int]
  print (search (listArray (0,n-1) xs) target 0 (n-1))
''',
'IPOP_5567': '''import qualified Data.IntSet as S
pairs (a:b:xs) = (a,b) : (b,a) : pairs xs
pairs _ = []
main = do
  (_:m:xs) <- fmap (map read . words) getContents :: IO [Int]
  let edges = pairs (take (2*m) xs)
      direct = S.fromList [b | (a,b) <- edges, a==1]
      two = S.fromList [b | (a,b) <- edges, S.member a direct]
  print (S.size (S.delete 1 (S.union direct two)))
''',
}

PL_IO = ''':- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \\n\\r\\t", " \\n\\r\\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
'''
PL = {
'IPOP_2609': '''gcd_value(A, 0, A) :- !.
gcd_value(A, B, G) :- R is A mod B, gcd_value(B, R, G).
main :- read_numbers([A,B]), gcd_value(A,B,G), L is (A // G)*B, writeln(G), writeln(L).
''',
'IPOP_1929': '''prime(N) :- N >= 2, trial(N,2).
trial(N,D) :- (D*D > N -> true ; N mod D =\\= 0, E is D+1, trial(N,E)).
main :- read_numbers([L,H]), forall((between(L,H,N),prime(N)),writeln(N)).
''',
'LC_0338': '''ones(0,0) :- !.
ones(N,C) :- Q is N//2, ones(Q,D), C is D + N mod 2.
main :- read_numbers([N]), findall(C,(between(0,N,I),ones(I,C)),Cs), write_numbers(Cs).
''',
'IPOP_10988': '''palindrome(Codes) :- reverse(Codes, Codes).
main :- read_words([Word]), string_codes(Word,Codes), (palindrome(Codes) -> writeln(1) ; writeln(0)).
''',
'IPOP_9012': '''balanced([],0).
balanced([40|Xs],D) :- E is D+1, balanced(Xs,E).
balanced([41|Xs],D) :- D > 0, E is D-1, balanced(Xs,E).
answer(S) :- string_codes(S,C), (balanced(C,0) -> writeln('YES') ; writeln('NO')).
main :- read_words([_|Words]), maplist(answer,Words).
''',
'LC_0242': '''frequencies(S,F) :- string_codes(S,C), msort(C,Sorted), clumped(Sorted,F).
main :- read_words([A,B]), frequencies(A,FA), frequencies(B,FB), (FA=FB -> writeln(1) ; writeln(0)).
''',
'LC_0217': '''has_duplicate([A,A|_]) :- !.
has_duplicate([_|Xs]) :- has_duplicate(Xs).
main :- read_numbers([_|Xs]), msort(Xs,Sorted), (has_duplicate(Sorted) -> writeln(1) ; writeln(0)).
''',
'LC_0283': '''nonzero(X) :- X =\\= 0.
main :- read_numbers([N|Xs]), include(nonzero,Xs,Kept), length(Kept,K), Z is N-K,
        length(Zeroes,Z), maplist(=(0),Zeroes), append(Kept,Zeroes,Out), write_numbers(Out).
''',
'LC_0912': '''merge_lists([],B,B) :- !.
merge_lists(A,[],A) :- !.
merge_lists([A|As],[B|Bs],[A|Cs]) :- A =< B, !, merge_lists(As,[B|Bs],Cs).
merge_lists([A|As],[B|Bs],[B|Cs]) :- merge_lists([A|As],Bs,Cs).
merge_sort([],[]) :- !.
merge_sort([X],[X]) :- !.
merge_sort(Xs,Ys) :- length(Xs,N), H is N//2, length(A,H), append(A,B,Xs),
                    merge_sort(A,SA), merge_sort(B,SB), merge_lists(SA,SB,Ys).
main :- read_numbers([_|Xs]), merge_sort(Xs,Ys), write_numbers(Ys).
''',
'IPOP_2579': '''stairs([],_,Prev,One,Two,Best) :- Best is max(One,Two), Prev >= 0.
stairs([X|Xs],PrevBest,PrevScore,One,Two,Best) :-
    NewOne is PrevBest+X, NewTwo is One+X, Current is max(One,Two),
    stairs(Xs,Current,PrevScore,NewOne,NewTwo,Best).
main :- read_numbers([_|[A|Xs]]), stairs(Xs,0,A,A,A,Best), writeln(Best).
''',
'LC_0062': '''next_row([_|Xs],[1|Ys]) :- row_tail(Xs,1,Ys).
row_tail([],_,[]).
row_tail([X|Xs],Left,[Y|Ys]) :- Y is X+Left, row_tail(Xs,Y,Ys).
rows(1,Row,Row) :- !.
rows(M,Row,Out) :- next_row(Row,Next), K is M-1, rows(K,Next,Out).
main :- read_numbers([M,N]), length(First,N), maplist(=(1),First), rows(M,First,Last), last(Last,Answer), writeln(Answer).
''',
'LC_0053': '''kadane([],_,Best,Best).
kadane([X|Xs],Ending,Best,Answer) :- E is max(X,Ending+X), B is max(Best,E), kadane(Xs,E,B,Answer).
main :- read_numbers([_,X|Xs]), kadane(Xs,X,X,Answer), writeln(Answer).
''',
'LC_0547': ''':- use_module(library(ordsets)).
matrix_rows([],_,[]).
matrix_rows(Xs,N,[Row|Rows]) :- length(Row,N), append(Row,Rest,Xs), matrix_rows(Rest,N,Rows).
visit([],_,Seen,Seen).
visit([V|Todo],Rows,Seen,Out) :-
    (ord_memberchk(V,Seen) -> visit(Todo,Rows,Seen,Out)
    ; nth1(V,Rows,Row), findall(J,nth1(J,Row,1),Neighbors), append(Neighbors,Todo,Next),
      ord_add_element(Seen,V,Added), visit(Next,Rows,Added,Out)).
components(I,N,_,_,0) :- I > N, !.
components(I,N,Rows,Seen,Count) :- J is I+1,
    (ord_memberchk(I,Seen) -> components(J,N,Rows,Seen,Count)
    ; visit([I],Rows,Seen,Next), components(J,N,Rows,Next,C), Count is C+1).
main :- read_numbers([N|Xs]), matrix_rows(Xs,N,Rows), components(1,N,Rows,[],C), writeln(C).
''',
'LC_0704': '''search(_,_,L,H,-1) :- L > H, !.
search(A,T,L,H,R) :- M is (L+H)//2, P is M+1, arg(P,A,V),
    (V =:= T -> R=M ; V < T -> K is M+1, search(A,T,K,H,R) ; K is M-1, search(A,T,L,K,R)).
main :- read_numbers([N,T|Xs]), A =.. [array|Xs], H is N-1, search(A,T,0,H,R), writeln(R).
''',
'IPOP_5567': '''edges([],[]).
edges([A,B|Xs],[A-B,B-A|Es]) :- edges(Xs,Es).
main :- read_numbers([_,_|Xs]), edges(Xs,Es),
        findall(B,member(1-B,Es),Direct),
        findall(C,(member(A,Direct),member(A-C,Es)),Second),
        append(Direct,Second,All), sort(All,Unique), delete(Unique,1,Invited), length(Invited,N), writeln(N).
''',
}

def main():
    records = []
    for group, ids in GROUPS.items():
        for pid in ids:
            source, dest = ROOT/'problem'/pid, DEST/pid
            dest.mkdir(parents=True, exist_ok=True)
            for name in ['statement.md', 'reference.cpp']:
                shutil.copy2(source/name, dest/name)
            for name in ['evaluation', 'prompt_examples']:
                shutil.copytree(source/name, dest/name, dirs_exist_ok=True)
            (dest/'reference.hs').write_text(HS[pid], encoding='utf-8', newline='\n')
            (dest/'reference.pl').write_text(PL_IO+PL[pid], encoding='utf-8', newline='\n')
            records.append({'problem_id':pid, 'group':group, 'pilot':pid in PILOT,
                            'selection_reason':'Three-language deterministic stdin/stdout; balanced prespecified domain',
                            'evaluation_cases':len(list((dest/'evaluation').glob('*.inp')))})
    excluded = [{'problem_id':p.name,'reason':'Not selected for the balanced 3-per-domain 15-problem design; no translation results consulted'}
                for p in sorted((ROOT/'problem').iterdir()) if (p/'reference.cpp').exists() and p.name not in HS]
    (DEST/'selection.json').write_text(json.dumps({'problems':records,'excluded':excluded,'pilot_problem_ids':PILOT},indent=2),encoding='utf-8')
    print(f'Prepared {len(records)} problems, {sum(r["evaluation_cases"] for r in records)} evaluation inputs')

if __name__ == '__main__':
    main()
