main :-
    read_line_codes(S),
    read_line_codes(T),
    msort(S, SS),
    msort(T, TT),
    ( SS == TT -> R = 1 ; R = 0 ),
    format("~w~n", [R]).

read_line_codes(Codes) :-
    get_char(C),
    read_line_codes_loop(C, Codes).

read_line_codes_loop(end_of_file, []) :- !.
read_line_codes_loop('\n', []) :- !.
read_line_codes_loop('\r', Codes) :- !,
    get_char(C2),
    read_line_codes_loop(C2, Codes).
read_line_codes_loop(C, [Code|Codes]) :-
    char_code(C, Code),
    get_char(C2),
    read_line_codes_loop(C2, Codes).