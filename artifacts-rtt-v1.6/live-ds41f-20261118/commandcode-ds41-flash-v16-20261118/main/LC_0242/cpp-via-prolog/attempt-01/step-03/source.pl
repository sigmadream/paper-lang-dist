main :-
    read_line_codes(S0),
    read_line_codes(T0),
    strip_cr(S0, S),
    strip_cr(T0, T),
    msort(S, SS),
    msort(T, TT),
    (   SS == TT
    ->  Result = 1
    ;   Result = 0
    ),
    write(Result),
    nl.

read_line_codes(Codes) :-
    get_code(user_input, C),
    read_line_codes(C, Codes).

read_line_codes(end_of_file, []) :- !.
read_line_codes(10, []) :- !.
read_line_codes(C, [C|Codes]) :-
    get_code(user_input, Next),
    read_line_codes_cont(Next, Codes).

read_line_codes_cont(end_of_file, []) :- !.
read_line_codes_cont(10, []) :- !.
read_line_codes_cont(C, [C|Codes]) :-
    get_code(user_input, Next),
    read_line_codes_cont(Next, Codes).

strip_cr([], []).
strip_cr([13|Cs], R) :-
    strip_cr(Cs, R).
strip_cr([C|Cs], [C|R]) :-
    C \= 13,
    strip_cr(Cs, R).