:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
gcd_value(A, 0, A) :- !.
gcd_value(A, B, G) :- R is A mod B, gcd_value(B, R, G).
main :- read_numbers([A,B]), gcd_value(A,B,G), L is (A // G)*B, writeln(G), writeln(L).
