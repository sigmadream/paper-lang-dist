read_line_codes(Codes) :-
    get_code(user_input, C),
    read_line_codes_(C, Codes).

read_line_codes_(end_of_file, []) :- !.
read_line_codes_(-1, []) :- !.
read_line_codes_(10, []) :- !.
read_line_codes_(C, [C|Rest]) :-
    get_code(user_input, C2),
    read_line_codes_(C2, Rest).

digits([], []).
digits([C|Cs], [C|Ds]) :-
    C >= 48,
    C =< 57,
    !,
    digits(Cs, Ds).
digits([_|Cs], Ds) :-
    digits(Cs, Ds).

number_from_codes(Codes, N) :-
    digits(Codes, Digits),
    number_codes(N, Digits).

check_parens(Codes) :-
    check_parens(Codes, 0).

check_parens([], 0).
check_parens([C|Cs], B) :-
    ( C =:= 40 ->
        B1 is B + 1,
        check_parens(Cs, B1)
    ; C =:= 41 ->
        B > 0,
        B1 is B - 1,
        check_parens(Cs, B1)
    ; check_parens(Cs, B)
    ).

process(0) :- !.
process(T) :-
    read_line_codes(Line),
    ( check_parens(Line) ->
        write('YES'), nl
    ;
        write('NO'), nl
    ),
    T1 is T - 1,
    process(T1).

main :-
    read_line_codes(First),
    number_from_codes(First, T),
    process(T).