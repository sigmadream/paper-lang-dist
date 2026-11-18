:- module(main, [main/0]).
:- use_module(library(charsio)).
:- use_module(library(dcgs)).
:- use_module(library(pio)).

gcd_(X, 0, X) :- !.
gcd_(X, Y, R) :- Z is X mod Y, gcd_(Y, Z, R).

main :-
    phrase_from_file(seq(Line), "user_input"),
    split_string(Line, " ", " ", Parts),
    maplist(number_string, [A, B], Parts),
    gcd_(A, B, G),
    L is (A // G) * B,
    format("~d~n~d~n", [G, L]).