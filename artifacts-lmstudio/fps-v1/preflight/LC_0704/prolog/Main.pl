:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
search(_,_,L,H,-1) :- L > H, !.
search(A,T,L,H,R) :- M is (L+H)//2, P is M+1, arg(P,A,V),
    (V =:= T -> R=M ; V < T -> K is M+1, search(A,T,K,H,R) ; K is M-1, search(A,T,L,K,R)).
main :- read_numbers([N,T|Xs]), A =.. [array|Xs], H is N-1, search(A,T,0,H,R), writeln(R).
