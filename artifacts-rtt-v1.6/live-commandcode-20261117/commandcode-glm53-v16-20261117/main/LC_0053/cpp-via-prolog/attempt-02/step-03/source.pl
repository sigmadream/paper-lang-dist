:- module(main, [main/0]).
:- use_module(library(readutil)).

main :-
    current_input(In),
    read_line_to_string(In, Line1),
    ( Line1 == end_of_file ->
        true
    ;
        read_line_to_string(In, Line2),
        split_string(Line2, " ", " ", Tokens),
        maplist(number_string, A, Tokens),
        A = [First|Rest],
        foldl(step, Rest, First-First, _-Best),
        format("~d~n", [Best])
    ).

step(X, Cur0-Best0, Cur-Best) :-
    Cur1 is max(X, Cur0 + X),
    Best is max(Best0, Cur1),
    Cur = Cur1.