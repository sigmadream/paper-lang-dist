main :-
    read_line_to_codes(user_input, T0),
    (   T0 == end_of_file
    ->  true
    ;   include(is_digit_code, T0, TDigits),
        number_codes(T, TDigits),
        process_cases(T)
    ).

is_digit_code(C) :-
    C >= 48,
    C =< 57.

process_cases(0) :- !.
process_cases(N) :-
    read_line_to_codes(user_input, Codes0),
    (   Codes0 == end_of_file
    ->  Codes = []
    ;   Codes = Codes0
    ),
    (   valid_parentheses(Codes)
    ->  write('YES')
    ;   write('NO')
    ),
    nl,
    N1 is N - 1,
    process_cases(N1).

valid_parentheses(Codes) :-
    valid_loop(Codes, 0, Final),
    Final =:= 0.

valid_loop([], Bal, Bal).
valid_loop([C|Cs], Bal, Final) :-
    (   C =:= 40
    ->  Bal1 is Bal + 1
    ;   C =:= 41
    ->  Bal1 is Bal - 1
    ;   Bal1 = Bal
    ),
    Bal1 >= 0,
    valid_loop(Cs, Bal1, Final).