:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, Codes),
    (   Codes == end_of_file
    ->  true
    ;   number_codes(N, Codes),
        count_solutions(0, N, 0, 0, 0, 0, Ans),
        format("~w~n", [Ans])
    ).

count_solutions(R, N, Cols, D1, D2, Acc, Res) :-
    (   R =:= N
    ->  Res is Acc + 1
    ;   count_cols(0, N, R, Cols, D1, D2, Acc, Res)
    ).

count_cols(C, N, _, _, _, _, Acc, Acc) :-
    C >= N.
count_cols(C, N, R, Cols, D1, D2, Acc, Res) :-
    C < N,
    Bc is 1 << C,
    Bd1 is 1 << (R + C),
    Bd2 is 1 << (R - C + N - 1),
    (   (Cols /\ Bc) =:= 0,
        (D1 /\ Bd1) =:= 0,
        (D2 /\ Bd2) =:= 0
    ->  Cols1 is Cols \/ Bc,
        D11 is D1 \/ Bd1,
        D21 is D2 \/ Bd2,
        R1 is R + 1,
        count_solutions(R1, N, Cols1, D11, D21, Acc, Acc1),
        C1 is C + 1,
        count_cols(C1, N, R, Cols, D1, D2, Acc1, Res)
    ;   C1 is C + 1,
        count_cols(C1, N, R, Cols, D1, D2, Acc, Res)
    ).