main :-
    read_line_to_string(user_input, L0),
    (   L0 == end_of_file
    ->  true
    ;   atom_string(A0, L0),
        atom_number(A0, T),
        process(T)
    ).

process(0) :- !.
process(N) :-
    N > 0,
    read_line_to_string(user_input, L),
    (   L == end_of_file
    ->  true
    ;   valid_braces(L, Ans),
        write(Ans), nl,
        N1 is N - 1,
        process(N1)
    ).

valid_braces(Line, 'YES') :-
    string_codes(Line, Cs),
    Cs \= [],
    valid_codes(Cs, 0),
    !.
valid_braces(_, 'NO').

valid_codes([], Bal) :-
    Bal =:= 0.
valid_codes([C|Cs], Bal) :-
    C =:= 40,
    Bal1 is Bal + 1,
    valid_codes(Cs, Bal1).
valid_codes([C|Cs], Bal) :-
    C =:= 41,
    Bal > 0,
    Bal1 is Bal - 1,
    valid_codes(Cs, Bal1).