:- module(main, [main/0]).
:- use_module(library(charsio)).

hanoi(1, S, _, E, [[S, E]|Ms], Ms) :- !.
hanoi(N, S, M, E, Acc0, Acc) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, S, E, M, Acc0, Acc1),
    Acc1 = [[S, E]|Acc2],
    hanoi(N1, M, S, E, Acc2, Acc).

read_n(N) :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file -> N = 0
    ; split_string(Line, " \t\r\n", " \t\r\n", Parts),
      ( Parts == [] -> N = 0
      ; [P|_] = Parts, number_string(N, P)
      )
    ).

main :-
    read_n(N),
    ( N >= 1 ->
        hanoi(N, 1, 2, 3, Moves, []),
        length(Moves, C),
        format("~d~n", [C]),
        forall(member([A, B], Moves),
               format("~d ~d~n", [A, B]))
    ; true
    ).