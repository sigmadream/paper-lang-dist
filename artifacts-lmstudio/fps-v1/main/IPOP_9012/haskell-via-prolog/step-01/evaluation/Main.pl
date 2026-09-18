balanced([], Depth, 0).
balanced([C|Cs], Depth, Acc) :-
    (   C == '(' ->
        NewDepth is Depth + 1,
        balanced(Cs, NewDepth, Acc)
    ;   C == ')' ->
        NewDepth is Depth - 1,
        NewAcc is Acc + 1,
        balanced(Cs, NewDepth, NewAcc)
    ),
    NewDepth >= 0.

main :-
    read_line(Input),
    length(Input, N),
    maplist(balanced(N), Input, Results),
    maplist(print_result, Results).

balanced(_, [], 0).
balanced(_, [C|Cs], Acc) :-
    (   C == '(' ->
        NewAcc is Acc + 1,
        balanced(_, Cs, NewAcc)
    ;   C == ')' ->
        NewAcc is Acc - 1,
        balanced(_, Cs, NewAcc)
    ),
    NewAcc >= 0.

print_result(true) :- write('YES'), nl.
print_result(false) :- write('NO'), nl.