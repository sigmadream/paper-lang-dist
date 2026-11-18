:- module(main, [main/0]).
:- use_module(library(charsio)).

hanoi(1, A, _, C, [[A, C] | Rest], Rest) :- !.
hanoi(N, A, B, C, Out, Rest) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, A, C, B, Out, Tmp),
    Tmp = [[A, C] | Tmp2],
    hanoi(N1, B, A, C, Tmp2, Rest).

main :-
    current_input(In),
    read_line_to_string(In, Line),
    ( Line == end_of_file -> true
    ; number_string(N, Line),
      ( N < 1 -> true
      ; M is (1 << N) - 1,
        format("~d~n", [M]),
        length(Moves, M),
        hanoi(N, 1, 2, 3, Moves, []),
        forall(member([A, C], Moves),
               format("~d ~d~n", [A, C]))
      )
    ).