:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
ones(0,0) :- !.
ones(N,C) :- Q is N//2, ones(Q,D), C is D + N mod 2.
main :- read_numbers([N]), findall(C,(between(0,N,I),ones(I,C)),Cs), write_numbers(Cs).
