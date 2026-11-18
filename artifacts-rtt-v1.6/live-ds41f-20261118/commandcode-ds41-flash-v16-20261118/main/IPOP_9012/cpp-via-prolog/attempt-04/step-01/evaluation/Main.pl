main :-
    read_line_to_string(user_input, TLine),
    (   TLine == end_of_file
    ->  true
    ;   number_string(T, TLine),
        process(T)
    ).

process(0) :- !.
process(N) :-
    read_line_to_string(user_input, S),
    (   S == end_of_file
    ->  true
    ;   (   valid_parens(S)
        ->  writeln('YES')
        ;   writeln('NO')
        ),
        N1 is N - 1,
        process(N1)
    ).

valid_parens(S) :-
    string_chars(S, Chars),
    check(Chars, 0).

check([], 0).
check(['('|Rest], Bal) :-
    Bal1 is Bal + 1,
    check(Rest, Bal1).
check([')'|Rest], Bal) :-
    Bal > 0,
    Bal1 is Bal - 1,
    check(Rest, Bal1).