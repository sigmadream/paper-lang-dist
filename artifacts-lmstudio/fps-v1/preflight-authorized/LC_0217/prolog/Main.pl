:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
has_duplicate([A,A|_]) :- !.
has_duplicate([_|Xs]) :- has_duplicate(Xs).
main :- read_numbers([_|Xs]), msort(Xs,Sorted), (has_duplicate(Sorted) -> writeln(1) ; writeln(0)).
