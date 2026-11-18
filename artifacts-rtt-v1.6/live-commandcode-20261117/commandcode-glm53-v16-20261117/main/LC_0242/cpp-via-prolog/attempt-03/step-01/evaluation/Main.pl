:- module(main, [main/0]).
:- use_module(library(aggregate)).

main :-
    current_input(In),
    read_line_to_codes(In, S),
    read_line_to_codes(In, T),
    ( ( var(S) ; var(T) ) ->
        true
    ;
        ( is_anagram(S, T) -> R = 1 ; R = 0 ),
        format("~d~n", [R])
    ).

is_anagram(S, T) :-
    msort(S, SS),
    msort(T, TT),
    SS == TT.