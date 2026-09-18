:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
nonzero(X) :- X =\= 0.
main :- read_numbers([N|Xs]), include(nonzero,Xs,Kept), length(Kept,K), Z is N-K,
        length(Zeroes,Z), maplist(=(0),Zeroes), append(Kept,Zeroes,Out), write_numbers(Out).
