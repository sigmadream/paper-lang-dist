:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, string).

hanoi(0, _, _, _, Acc, Acc) :- nil.
hanoi(N, A, B, C, Acc0, Acc) :-
    N > 0,
    N1 is N - 1,
    hanoi(N1, A, C, B, Acc0, Acc1),
    Acc2 = [ (A-C) | Acc1 ],
    hanoi(N1, B, A, C, Acc2, Acc).

main :-
    current_input(In),
    read_line_to_string(In, Line),
    ( Line == end_of_file -> true
    ; number_string(N, Line),
      hanoi(N, 1, 2, 3, [], Rev),
      reverse(Rev, Moves),
      length(Moves, Count),
      format("~d~n", [Count]),
      forall(member(A-B, Moves),
             format("~w ~w~n", [A, B]))
    ).