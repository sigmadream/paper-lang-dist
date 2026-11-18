:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, TStr),
    number_string(T, TStr),
    process(T).

process(0) :- !.
process(N) :-
    read_line_to_string(user_input, Line),
    (   valid(Line) -> writeln('YES') ; writeln('NO') ),
    N1 is N - 1,
    process(N1).

valid(Line) :-
    string_chars(Line, Chars),
    scan(Chars, 0).

scan([], 0).
scan([C|Cs], Bal) :-
    (   C = '(' ->
        Bal1 is Bal + 1,
        scan(Cs, Bal1)
    ;   C = ')' ->
        Bal > 0,
        Bal1 is Bal - 1,
        scan(Cs, Bal1)
    ;   scan(Cs, Bal)
    ).