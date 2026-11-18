:- module(main, [main/0]).

main :-
    read_line_to_codes(user_input, Line1),
    (   Line1 = end_of_file
    ->  true
    ;   number_codes(T, Line1),
        process_lines(T)
    ).

process_lines(0) :- !.
process_lines(N) :-
    read_line_to_codes(user_input, Line),
    (   Line = end_of_file
    ->  true
    ;   (   valid(Line)
        ->  write('YES'), nl
        ;   write('NO'), nl
        ),
        N1 is N - 1,
        process_lines(N1)
    ).

valid(Codes) :-
    loop(Codes, 0).

loop([], 0).
loop([0'(|Rest], Bal) :-
    Bal1 is Bal + 1,
    loop(Rest, Bal1).
loop([0')|Rest], Bal) :-
    Bal > 0,
    Bal1 is Bal - 1,
    loop(Rest, Bal1).