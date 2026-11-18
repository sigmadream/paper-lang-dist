:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, atom).

main :-
    current_input(In),
    read_line_to_codes(In, Line),
    ( Line == end_of_file -> true
    ; split_string(Line, " ", " ", Parts),
      maplist(number_string, [A,B], Parts),
      gcd(A, B, G),
      L is (A // G) * B,
      format("~d~n~d~n", [G, L])
    ).

gcd(A, 0, A) :- !.
gcd(A, B, G) :- C is A mod B, gcd(B, C, G).