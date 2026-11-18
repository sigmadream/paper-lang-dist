:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
hanoi(0,_,_,_) :- !.
hanoi(N,A,B,C) :- K is N-1, hanoi(K,A,C,B), format('~d ~d~n',[A,C]), hanoi(K,B,A,C).
main :- read_numbers([N]), Count is (1<<N)-1, writeln(Count), hanoi(N,1,2,3).
