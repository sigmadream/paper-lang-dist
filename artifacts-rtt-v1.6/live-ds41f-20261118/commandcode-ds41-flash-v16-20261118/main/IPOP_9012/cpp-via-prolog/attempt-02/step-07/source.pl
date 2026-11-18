main :-
    read_line_to_string(user_input, TLine),
    (   TLine == end_of_file
    ->  true
    ;   number_string(T, TLine),
        process_cases(T)
    ).

process_cases(0) :- !.
process_cases(N) :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   (   valid_parentheses(Line)
        ->  writeln('YES')
        ;   writeln('NO')
        ),
        N1 is N - 1,
        process_cases(N1)
    ).

valid_parentheses(Line) :-
    string_codes(Line, Codes),
    valid_codes(Codes, 0).

valid_codes([], 0) :- !.
valid_codes([40|Rest], Bal) :-
    !,
    Bal1 is Bal + 1,
    valid_codes(Rest, Bal1).
valid_codes([41|Rest], Bal) :-
    !,
    (   Bal > 0
    ->  Bal1 is Bal - 1,
        valid_codes(Rest, Bal1)
    ;   fail
    ).
valid_codes([_|Rest], Bal) :-
    valid_codes(Rest, Bal).