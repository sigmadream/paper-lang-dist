main :-
    read_line_to_string(user_input, First),
    (   First == end_of_file
    ->  true
    ;   number_string(T, First),
        process_cases(T)
    ).

process_cases(0) :- !.
process_cases(N) :-
    N > 0,
    read_line_to_string(user_input, S),
    (   S == end_of_file
    ->  true
    ;   check_string(S)
    ),
    N1 is N - 1,
    process_cases(N1).

check_string(S) :-
    string_chars(S, Chars),
    balance(Chars, 0, Ok),
    (   Ok == true
    ->  format('YES~n')
    ;   format('NO~n')
    ).

balance([], B, Result) :-
    (   B =:= 0
    ->  Result = true
    ;   Result = false
    ).
balance(['('|T], B, Result) :-
    B1 is B + 1,
    balance(T, B1, Result).
balance([')'|T], B, Result) :-
    B > 0,
    B1 is B - 1,
    balance(T, B1, Result).
balance([')'|_], 0, false).