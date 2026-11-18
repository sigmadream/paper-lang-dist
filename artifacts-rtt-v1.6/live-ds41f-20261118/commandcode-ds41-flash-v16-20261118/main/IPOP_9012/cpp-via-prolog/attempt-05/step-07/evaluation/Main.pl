:- use_module(library(readutil)).

main :-
    read_line_to_string(current_input, First),
    (   First == end_of_file
    ->  true
    ;   trim_string(First, Trimmed),
        (   string_codes(Trimmed, [])
        ->  true
        ;   number_string(T, Trimmed),
            process(T)
        )
    ).

process(0) :- !.
process(N) :-
    read_line_to_string(current_input, Line),
    (   Line == end_of_file
    ->  true
    ;   strip_cr(Line, L2),
        (   valid_parentheses(L2)
        ->  writeln('YES')
        ;   writeln('NO')
        ),
        N1 is N - 1,
        process(N1)
    ).

trim_string(S, Trimmed) :-
    string_codes(S, Codes),
    trim_left(Codes, C1),
    reverse(C1, Rev),
    trim_left(Rev, Rev2),
    reverse(Rev2, C2),
    string_codes(Trimmed, C2).

trim_left([C|T], Out) :-
    (   C =:= 32
    ;   C =:= 9
    ;   C =:= 13
    ;   C =:= 10
    ),
    !,
    trim_left(T, Out).
trim_left(L, L).

strip_cr(S, Out) :-
    string_codes(S, Codes),
    reverse(Codes, Rev),
    (   Rev = [13|Rest]
    ->  reverse(Rest, Codes2)
    ;   Codes2 = Codes
    ),
    string_codes(Out, Codes2).

valid_parentheses(S) :-
    string_codes(S, Codes),
    valid_balance(Codes, 0).

valid_balance([], B) :-
    B =:= 0.
valid_balance([40|T], B) :-
    B1 is B + 1,
    valid_balance(T, B1).
valid_balance([41|T], B) :-
    B > 0,
    B1 is B - 1,
    valid_balance(T, B1).