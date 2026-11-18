main :-
    read_string(user_input, end_of_file, Str),
    string_codes(Str, Codes),
    parse_numbers(Codes, Numbers),
    Numbers = [_N, C | Homes],
    sort(Homes, Sorted),
    Sorted = [First|_],
    last_elem(Sorted, Last),
    High is Last - First,
    binary_search(Sorted, C, 1, High, 0, Answer),
    format("~w~n", [Answer]).

last_elem([X], X).
last_elem([_|T], X) :-
    last_elem(T, X).

parse_numbers([], []).
parse_numbers([C|Cs], Ns) :-
    C =< 32,
    !,
    parse_numbers(Cs, Ns).
parse_numbers(Cs, [N|Ns]) :-
    parse_uint(Cs, N, Rest),
    parse_numbers(Rest, Ns).

parse_uint([C|Cs], N, Rest) :-
    C >= 48,
    C =< 57,
    N0 is C - 48,
    parse_uint_digits(Cs, N0, N, Rest).

parse_uint_digits([C|Cs], Acc, N, Rest) :-
    C >= 48,
    C =< 57,
    !,
    Acc1 is Acc * 10 + (C - 48),
    parse_uint_digits(Cs, Acc1, N, Rest).
parse_uint_digits(Rest, N, N, Rest).

binary_search(_, _, Low, High, Ans, Ans) :-
    Low > High,
    !.
binary_search(Homes, C, Low, High, Ans, Result) :-
    Mid is Low + (High - Low) // 2,
    ( possible(Homes, C, Mid) ->
        Low1 is Mid + 1,
        binary_search(Homes, C, Low1, High, Mid, Result)
    ;   High1 is Mid - 1,
        binary_search(Homes, C, Low, High1, Ans, Result)
    ).

possible(Homes, C, Dist) :-
    Homes = [Prev|Rest],
    possible_scan(Rest, Prev, 1, C, Dist).

possible_scan(_, _, Count, C, _) :-
    Count >= C,
    !.
possible_scan([], _, Count, C, _) :-
    Count >= C.
possible_scan([H|Hs], Prev, Count, C, Dist) :-
    ( H - Prev >= Dist ->
        Count1 is Count + 1,
        possible_scan(Hs, H, Count1, C, Dist)
    ;   possible_scan(Hs, Prev, Count, C, Dist)
    ).