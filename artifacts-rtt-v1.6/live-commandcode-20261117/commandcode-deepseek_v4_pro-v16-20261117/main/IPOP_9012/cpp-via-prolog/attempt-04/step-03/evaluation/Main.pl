:- use_module(library(readutil)).

main :-
    read_line_to_string(current_input, TLine),
    (   TLine = end_of_file
    ->  true
    ;   number_string(T, TLine),
        process(T)
    ).

process(0) :- !.
process(T) :-
    read_line_to_string(current_input, Line),
    (   Line = end_of_file
    ->  true
    ;   (   check_line(Line)
        ->  writeln('YES')
        ;   writeln('NO')
        ),
        T1 is T - 1,
        process(T1)
    ).

check_line(Line) :-
    string_chars(Line, Chars),
    check_balance(Chars, 0).

check_balance([], B) :-
    B =:= 0.
check_balance([C|Cs], B) :-
    (   C = '('
    ->  B1 is B + 1
    ;   C = ')'
    ->  B1 is B - 1
    ;   fail
    ),
    (   B1 < 0
    ->  fail
    ;   check_balance(Cs, B1)
    ).