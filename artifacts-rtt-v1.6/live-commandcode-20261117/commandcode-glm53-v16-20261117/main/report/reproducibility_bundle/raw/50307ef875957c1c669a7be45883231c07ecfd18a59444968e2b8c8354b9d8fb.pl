:- module(main, []).
:- use_module(library(aggregate)).

main :-
    read_line(S),
    read_line(T),
    ( anagram(S, T) -> R = 1 ; R = 0 ),
    format("~d~n", [R]).

read_line(L) :-
    read_line_to_codes(user_input, Cs),
    ( Cs == end_of_file -> L = [] ; L = Cs ).

anagram([], []).
anagram([C|S], T) :-
    memberchk(C, T0),
    select(C, T, T0),
    !,
    anagram(S, T0).
anagram([], _) :- !, fail.
anagram(_, []) :- !, fail.