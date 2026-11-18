:- use_module(library(readutil)).

gcd(A, 0, A) :-
    A > 0.
gcd(A, B, G) :-
    B > 0,
    R is A mod B,
    gcd(B, R, G).

remove_empty([], []).
remove_empty([H|T], R) :-
    ( H == "" ->
        remove_empty(T, R)
    ;
        R = [H|R1],
        remove_empty(T, R1)
    ).

main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", Parts),
    remove_empty(Parts, Tokens),
    Tokens = [AStr, BStr|_],
    atom_string(AA, AStr),
    atom_number(AA, A),
    atom_string(BA, BStr),
    atom_number(BA, B),
    gcd(A, B, G),
    L is (A // G) * B,
    format("~d~n~d~n", [G, L]).