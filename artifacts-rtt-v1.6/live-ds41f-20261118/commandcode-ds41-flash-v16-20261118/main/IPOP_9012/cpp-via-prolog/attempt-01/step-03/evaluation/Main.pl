:- module(main, [main/0]).

main :-
    read_line_to_string(user_input, First),
    (   First == end_of_file
    ->  true
    ;   number_string(T, First),
        loop(T)
    ).

loop(0) :- !.
loop(N) :-
    N > 0,
    read_line_to_string(user_input, S),
    (   S == end_of_file
    ->  true
    ;   (   check(S)
        ->  writeln('YES')
        ;   writeln('NO')
        ),
        N1 is N - 1,
        loop(N1)
    ).

check(S) :-
    string_length(S, L),
    L > 0,
    string_chars(S, Chars),
    valid(Chars, 0).

valid([], 0).
valid(['(' | T], B) :-
    B1 is B + 1,
    valid(T, B1).
valid([')' | T], B) :-
    B > 0,
    B1 is B - 1,
    valid(T, B1).