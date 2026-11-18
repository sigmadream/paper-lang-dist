main :-
    read_string(user_input, end_of_file, Input),
    split_string(Input, " \t\n\r", " \t\n\r", Tokens),
    Tokens = [SN, SC | CoordTokens],
    number_string(N, SN),
    number_string(C, SC),
    maplist(number_string, Coords, CoordTokens),
    sort(Coords, Sorted),
    Sorted = [First | _],
    last(Sorted, Last),
    MaxDist is Last - First,
    binary_search(Sorted, C, 1, MaxDist, 0, Answer),
    write(Answer),
    nl.

binary_search(_, _, Left, Right, Answer, Answer) :-
    Left > Right,
    !.
binary_search(Sorted, C, Left, Right, Current, Answer) :-
    Mid is Left + ((Right - Left) // 2),
    (   feasible(Mid, Sorted, C) ->
        NewLeft is Mid + 1,
        binary_search(Sorted, C, NewLeft, Right, Mid, Answer)
    ;   NewRight is Mid - 1,
        binary_search(Sorted, C, Left, NewRight, Current, Answer)
    ).

feasible(D, Sorted, C) :-
    Sorted = [First | Rest],
    count_rest(Rest, First, 1, C, D).

count_rest(_, _, Count, C, _) :-
    Count >= C,
    !.
count_rest([X | Xs], Prev, Count, C, D) :-
    (   X - Prev >= D ->
        Count1 is Count + 1,
        Prev1 = X
    ;   Count1 = Count,
        Prev1 = Prev
    ),
    count_rest(Xs, Prev1, Count1, C, D).