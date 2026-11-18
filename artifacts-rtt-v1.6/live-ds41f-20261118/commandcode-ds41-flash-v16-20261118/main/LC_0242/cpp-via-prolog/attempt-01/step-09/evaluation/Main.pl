main :-
    read_line_chars(S),
    read_line_chars(T),
    msort(S, SS),
    msort(T, TT),
    (   SS == TT
    ->  R = 1
    ;   R = 0
    ),
    write(R),
    nl.

read_line_chars(Chars) :-
    read_line_chars([], RevChars),
    reverse(RevChars, Chars0),
    strip_trailing_cr(Chars0, Chars).

read_line_chars(Acc, RevChars) :-
    get_char(C),
    (   C == end_of_file
    ->  RevChars = Acc
    ;   C == '\n'
    ->  RevChars = Acc
    ;   read_line_chars([C|Acc], RevChars)
    ).

strip_trailing_cr([], []).
strip_trailing_cr(Chars, Stripped) :-
    reverse(Chars, ['\r'|RestRev]),
    !,
    reverse(RestRev, Stripped).
strip_trailing_cr(Chars, Chars).