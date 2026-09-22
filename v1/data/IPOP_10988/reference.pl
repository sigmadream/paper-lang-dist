:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
palindrome(Codes) :- reverse(Codes, Codes).
main :- read_words([Word]), string_codes(Word,Codes), (palindrome(Codes) -> writeln(1) ; writeln(0)).
