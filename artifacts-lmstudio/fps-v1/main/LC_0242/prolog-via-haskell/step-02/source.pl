:- use_module(library(io)).

frequencies(S, F) :-
    string_to_list(S, L),
    findall((C, N), (member(C, L), count_char(L, C, N)), F).

count_char([], _, 0).
count_char([H|T], C, N) :-
    (   H = C -> N1 is N + 1 ; N1 = N ),
    count_char(T, C, N1).

main :-
    read_line_to_string(S),
    read_line_to_string(T),
    frequencies(S, FA),
    frequencies(T, FB),
    (   FA = FB -> write(1) ; write(0) ),
    nl.