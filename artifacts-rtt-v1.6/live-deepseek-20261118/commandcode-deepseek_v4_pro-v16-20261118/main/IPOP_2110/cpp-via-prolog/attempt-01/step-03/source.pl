main :-
    read(N),
    read(C),
    read_coords(N, Coords),
    sort(Coords, Sorted),
    Sorted = [First|_],
    last(Sorted, Last),
    Right is Last - First,
    binary_search(Sorted, C, 1, Right, 0, Ans),
    writeln(Ans).

read_coords(N, Coords) :-
    read_coords_acc(N, [], Rev),
    reverse(Rev, Coords).

read_coords_acc(0, Acc, Acc).
read_coords_acc(N, Acc, Coords) :-
    N > 0,
    read(X),
    N1 is N - 1,
    read_coords_acc(N1, [X|Acc], Coords).

binary_search(_, _, Left, Right, Ans, Ans) :- Left > Right, !.
binary_search(Sorted, C, Left, Right, Ans0, FinalAns) :-
    Mid is Left + (Right - Left) // 2,
    (   can_place(Sorted, Mid, C)
    ->  NewLeft is Mid + 1,
        binary_search(Sorted, C, NewLeft, Right, Mid, FinalAns)
    ;   NewRight is Mid - 1,
        binary_search(Sorted, C, Left, NewRight, Ans0, FinalAns)
    ).

can_place([First|Rest], Dist, C) :-
    can_place_iter(Rest, Dist, C, 1, First).

can_place_iter(_, _, C, Count, _) :- Count >= C, !.
can_place_iter([], _, _, Count, _) :- Count >= C.
can_place_iter([H|T], Dist, C, Count, Prev) :-
    (   H - Prev >= Dist
    ->  NewCount is Count + 1,
        can_place_iter(T, Dist, C, NewCount, H)
    ;   can_place_iter(T, Dist, C, Count, Prev)
    ).