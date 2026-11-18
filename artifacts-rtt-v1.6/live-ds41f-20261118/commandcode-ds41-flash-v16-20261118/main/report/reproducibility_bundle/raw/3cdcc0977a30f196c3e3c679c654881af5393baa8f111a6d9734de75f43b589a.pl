is_ws(C) :-
    char_code(C, Code),
    ( Code =:= 32
    ; Code =:= 9
    ; Code =:= 10
    ; Code =:= 13
    ; Code =:= 12
    ; Code =:= 11
    ).

skip_ws(end_of_file, end_of_file) :- !.
skip_ws(C, C1) :-
    is_ws(C), !,
    get_char(NC),
    skip_ws(NC, C1).
skip_ws(C, C).

read_token(Tok) :-
    get_char(C),
    skip_ws(C, C1),
    ( C1 == end_of_file ->
        Tok = end_of_file
    ; read_token_chars(C1, Chars),
      atom_chars(Tok, Chars)
    ).

read_token_chars(end_of_file, []) :- !.
read_token_chars(C, []) :-
    is_ws(C), !.
read_token_chars(C, [C|Rest]) :-
    get_char(NC),
    read_token_chars(NC, Rest).

valid_paren(S) :-
    atom_chars(S, Chars),
    check(Chars, 0).

check([], Bal) :-
    Bal =:= 0.
check(['('|Rest], Bal) :-
    Bal1 is Bal + 1,
    check(Rest, Bal1).
check([')'|Rest], Bal) :-
    Bal > 0,
    Bal1 is Bal - 1,
    check(Rest, Bal1).

process(0) :- !.
process(T) :-
    T > 0,
    read_token(S),
    ( S == end_of_file ->
        true
    ; valid_paren(S) ->
        write('YES'), nl
    ; write('NO'), nl
    ),
    T1 is T - 1,
    process(T1).

main :-
    read_token(Tok),
    ( Tok == end_of_file ->
        true
    ; atom_number(Tok, T),
      process(T)
    ).