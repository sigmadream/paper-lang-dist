hanoi_moves(N, From, Mid, To, Moves) :-
    hanoi_moves_dl(N, From, Mid, To, Moves, []).

hanoi_moves_dl(1, From, _, To, [(From, To)|T], T).
hanoi_moves_dl(N, From, Mid, To, Moves, Tail) :-
    N > 1,
    N1 is N - 1,
    hanoi_moves_dl(N1, From, To, Mid, Moves, T1),
    hanoi_moves_dl(N1, Mid, From, To, T2, Tail),
    T1 = [(From, To)|T2].

main :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        halt
    ; number_string(N, Line) ->
        hanoi_moves(N, 1, 2, 3, Moves),
        length(Moves, Count),
        write(Count), nl,
        forall(member((A, B), Moves),
               (write(A), write(' '), write(B), nl))
    ; halt
    ).