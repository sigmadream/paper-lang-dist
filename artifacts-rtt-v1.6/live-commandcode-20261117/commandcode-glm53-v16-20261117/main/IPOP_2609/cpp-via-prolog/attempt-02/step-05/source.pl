:- module(main, [main/0]).

main :-
    read_line_to_codes(user_input, Cs),
    ( Cs == end_of_file -> true
    ; split(Cs, Parts),
      maplist(number_codes, [A, B], Parts),
      gcd_(A, B, G),
      L is A // G * B,
      format("~d~n~d~n", [G, L])
    ).

split(Cs, Parts) :-
    split_codes(Cs, [], Parts).

split_codes([], Acc, [Part]) :- !,
    reverse(Acc, R),
    Part = R.
split_codes([C|T], Acc, Parts) :-
    ( C == 32 ; C == 10 ; C == 13 ; C == 9 ) ->
        ( Acc == [] -> split_codes(T, [], Parts)
        ; reverse(Acc, R), Parts = [R|Rest], split_codes(T, [], Rest)
        )
    ; split_codes(T, [C|Acc], Parts).

gcd_(A, 0, A) :- !.
gcd_(A, B, G) :- R is A mod B, gcd_(B, R, G).