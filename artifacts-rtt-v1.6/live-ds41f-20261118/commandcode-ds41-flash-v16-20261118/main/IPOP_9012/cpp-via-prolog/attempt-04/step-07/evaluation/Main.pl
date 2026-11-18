main :-
    current_input(In),
    read_line_to_codes(In, FirstLine),
    (   FirstLine == end_of_file
    ->  true
    ;   trim_codes(FirstLine, FirstTrim),
        (   number_codes(T, FirstTrim)
        ->  process_lines(In, T)
        ;   true
        )
    ).

process_lines(_, 0) :- !.
process_lines(In, N) :-
    N > 0,
    read_line_to_codes(In, Line),
    (   Line == end_of_file
    ->  true
    ;   trim_codes(Line, Trimmed),
        (   valid_parens(Trimmed)
        ->  writeln('YES')
        ;   writeln('NO')
        ),
        N1 is N - 1,
        process_lines(In, N1)
    ).

valid_parens(Codes) :-
    valid_parens(Codes, 0).

valid_parens([], Balance) :-
    Balance =:= 0.
valid_parens([40|Rest], Balance) :-
    Balance1 is Balance + 1,
    valid_parens(Rest, Balance1).
valid_parens([41|Rest], Balance) :-
    Balance > 0,
    Balance1 is Balance - 1,
    valid_parens(Rest, Balance1).
valid_parens([Code|Rest], Balance) :-
    Code =\= 40,
    Code =\= 41,
    valid_parens(Rest, Balance).

trim_codes(Codes, Trimmed) :-
    drop_ws_left(Codes, LeftTrimmed),
    reverse(LeftTrimmed, Reversed),
    drop_ws_left(Reversed, RightTrimmedReversed),
    reverse(RightTrimmedReversed, Trimmed).

drop_ws_left([Code|Rest], Out) :-
    is_ws(Code),
    !,
    drop_ws_left(Rest, Out).
drop_ws_left(Codes, Codes).

is_ws(Code) :-
    memberchk(Code, [9, 10, 11, 12, 13, 32]).