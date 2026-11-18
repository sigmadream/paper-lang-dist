:- module(main, [main/0]).
:- use_module(library(readutil)).

gcd_(A, 0, A) :- !.
gcd_(A, B, G) :- R is A mod B, gcd_(B, R, G).

main :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file -> true
    ; split_string(Line, " ", " \t\r\n", Parts),
      maplist(number_string, [A, B], Parts),
      gcd_(A, B, G),
      L is (A // G) * B,
      format("~d~n~d~n", [G, L])
    ).