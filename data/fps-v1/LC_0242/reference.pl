:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
frequencies(S,F) :- string_codes(S,C), msort(C,Sorted), clumped(Sorted,F).
main :- read_words([A,B]), frequencies(A,FA), frequencies(B,FB), (FA=FB -> writeln(1) ; writeln(0)).
