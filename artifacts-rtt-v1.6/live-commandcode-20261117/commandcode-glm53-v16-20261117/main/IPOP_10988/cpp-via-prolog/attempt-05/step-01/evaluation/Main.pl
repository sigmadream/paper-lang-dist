:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, atom).

main :-
    current_input(In),
    read_line_to_string(In, Line),
    (   Line == end_of_file
    ->  true
    ;   string_length(Line, N),
        (   palindrome(Line, N)
        ->  writeln(1)
        ;   writeln(0)
        )
    ).

palindrome(_, 1).
palindrome(Line, N) :-
    N > 1,
    Half is N // 2,
    check(Line, 0, Half).

check(_, I, Half) :- I >= Half, !.
check(Line, I, Half) :-
    I < Half,
    J is I + 1,
    string_code(I, Line, C1),
    K is Half * 2 - J + 1,  % not used; compute mirror below
    string_length(Line, N),
    Mirror is N - J,
    string_code(Mirror, Line, C2),
    C1 == C2,
    check(Line, J, Half).