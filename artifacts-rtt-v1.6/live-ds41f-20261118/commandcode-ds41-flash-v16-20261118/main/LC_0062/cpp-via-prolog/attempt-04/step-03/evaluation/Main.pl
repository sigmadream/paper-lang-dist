step([First|Rest], NewRow) :-
    step_acc(Rest, First, [First], Rev),
    reverse(Rev, NewRow).

step_acc([], _, Acc, Acc).
step_acc([C|Cs], Prev, Acc, Rev) :-
    V is Prev + C,
    step_acc(Cs, V, [V|Acc], Rev).

repeat_step(0, Row, Row).
repeat_step(K, Row, Out) :-
    K > 0,
    step(Row, Row2),
    K1 is K - 1,
    repeat_step(K1, Row2, Out).

make_ones(0, []).
make_ones(N, [1|T]) :-
    N > 0,
    N1 is N - 1,
    make_ones(N1, T).

compute(M, N, Ans) :-
    make_ones(N, Row),
    K is M - 1,
    repeat_step(K, Row, Final),
    last(Final, Ans).

main :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   split_string(Line, " \t\r\n", " \t\r\n", Tokens),
        Tokens = [MStr, NStr|_],
        number_string(M, MStr),
        number_string(N, NStr),
        compute(M, N, Ans),
        writeln(Ans)
    ).