:- module(main, []).
:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, S1),
    read_line_to_codes(user_input, S2),
    ( S1 == end_of_file -> S = [] ; S = S1 ),
    ( S2 == end_of_file -> T = [] ; T = S2 ),
    ( anagram(S, T) -> R = 1 ; R = 0 ),
    format("~d~n", [R]).

anagram(S, T) :- msort(S, A), msort(T, A).