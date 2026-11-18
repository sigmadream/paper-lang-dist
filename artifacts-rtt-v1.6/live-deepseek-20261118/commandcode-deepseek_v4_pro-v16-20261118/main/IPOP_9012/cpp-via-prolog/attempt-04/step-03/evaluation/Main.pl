main :-
    read_line_to_string(user_input, TLine),
    (   TLine == end_of_file
    ->  true
    ;   number_string(T, TLine),
        process(T)
    ).

process(0).
process(N) :-
    N > 0,
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   (   is_valid(Line)
        ->  format('YES~n')
        ;   format('NO~n')
        ),
        N1 is N-1,
        process(N1)
    ).

is_valid(Line) :-
    string_chars(Line, Chars),
    check_balance(Chars, 0).

check_balance([], 0).
check_balance(['('|Rest], Bal) :-
    Bal1 is Bal + 1,
    check_balance(Rest, Bal1).
check_balance([')'|Rest], Bal) :-
    Bal > 0,
    Bal1 is Bal - 1,
    check_balance(Rest, Bal1).