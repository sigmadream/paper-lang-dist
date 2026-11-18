:- use_module(library(readutil)).

main :-
    current_input(Stream),
    read_all_codes(Stream, Codes),
    lex(Codes, [_N|Nums]),
    Nums = [First|Rest],
    kadane(Rest, First, First, Best),
    write(Best), nl.

read_all_codes(Stream, Codes) :-
    read_line_to_codes(Stream, Line),
    (   Line == end_of_file
    ->  Codes = []
    ;   append(Line, [10|Rest], Codes),
        read_all_codes(Stream, Rest)
    ).

lex([], []).
lex([C|Cs], Rest) :-
    C =< 32, !,
    lex(Cs, Rest).
lex(Codes, [N|Ns]) :-
    parse_number(Codes, N, Rest),
    !,
    lex(Rest, Ns).

parse_number([C|Cs], N, Rest) :-
    (   C =:= 0'-
    ;   C >= 0'0, C =< 0'9
    ),
    parse_number_chars([C|Cs], Chars, Rest),
    number_codes(N, Chars).

parse_number_chars([C|Cs], [C|Chars], Rest) :-
    (   C =:= 0'-
    ;   C >= 0'0, C =< 0'9
    ),
    !,
    parse_number_chars(Cs, Chars, Rest).
parse_number_chars(Rest, [], Rest).

kadane([], _, Best, Best).
kadane([X|Xs], Cur, Best, Out) :-
    Cur1 is max(X, Cur + X),
    Best1 is max(Best, Cur1),
    kadane(Xs, Cur1, Best1, Out).