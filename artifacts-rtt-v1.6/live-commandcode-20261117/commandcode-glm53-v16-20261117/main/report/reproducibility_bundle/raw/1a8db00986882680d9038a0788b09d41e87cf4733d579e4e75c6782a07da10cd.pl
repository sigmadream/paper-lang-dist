:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
prime(N) :- N >= 2, trial(N,2).
trial(N,D) :- (D*D > N -> true ; N mod D =\= 0, E is D+1, trial(N,E)).
main :- read_numbers([L,H]), forall((between(L,H,N),prime(N)),writeln(N)).
