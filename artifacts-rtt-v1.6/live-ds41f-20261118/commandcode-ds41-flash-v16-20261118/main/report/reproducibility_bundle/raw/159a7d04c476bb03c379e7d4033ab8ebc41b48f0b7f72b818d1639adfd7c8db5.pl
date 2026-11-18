:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
balanced([],0).
balanced([40|Xs],D) :- E is D+1, balanced(Xs,E).
balanced([41|Xs],D) :- D > 0, E is D-1, balanced(Xs,E).
answer(S) :- string_codes(S,C), (balanced(C,0) -> writeln('YES') ; writeln('NO')).
main :- read_words([_|Words]), maplist(answer,Words).
