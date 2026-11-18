:- module(main, [main/0]).
:- use_module(library(readutil)).

gcd_(A, 0, A) :- !.
gcd_(A, B, G) :- R is A mod B, gcd_(B, R, G).

main :-
    current_input(In),
    read_line_to_string(In, Line),
    (   Line == end_of_file
    ->  true
    ;   split_string(Line, " ", "\s\t\r\n", Parts),
        maplist(number_string, [A, B], Parts),
        gcd_(A, B, G),
        L is (A // G) * B,
        format("~d~n~d~n", [G, L])
    ).