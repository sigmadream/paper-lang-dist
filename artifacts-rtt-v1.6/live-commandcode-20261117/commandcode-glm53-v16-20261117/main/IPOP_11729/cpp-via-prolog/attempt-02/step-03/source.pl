:- module(main, [main/0]).

hanoi(1, A, _, C, [[A, C]]).
hanoi(N, A, B, C, Moves) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, A, C, B, M1),
    hanoi(N1, B, A, C, M2),
    append(M1, [[A, C] | M2], Moves).

main :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file -> true
    ; number_string(N, Line),
      ( N < 1 -> true
      ; Moves is (1 << N) - 1,
        format("~d~n", [Moves]),
        hanoi(N, 1, 2, 3, L),
        forall(member([A, C], L), format("~d ~d~n", [A, C]))
      )
    ).