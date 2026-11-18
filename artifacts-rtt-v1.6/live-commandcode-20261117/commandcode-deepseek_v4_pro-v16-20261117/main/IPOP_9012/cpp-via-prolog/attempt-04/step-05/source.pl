main :-
    read(T),
    get_code(_), % consume newline after T
    process_lines(T).

process_lines(0).
process_lines(N) :-
    N > 0,
    read_line_to_string(user_input, Line),
    string_chars(Line, Chars),
    ( valid(Chars, 0) -> format('YES~n') ; format('NO~n') ),
    N1 is N - 1,
    process_lines(N1).

valid([], 0).
valid(['('|T], Bal) :-
    Bal1 is Bal + 1,
    valid(T, Bal1).
valid([')'|T], Bal) :-
    Bal > 0,
    Bal1 is Bal - 1,
    valid(T, Bal1).