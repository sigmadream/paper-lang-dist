main :-
    (   read_line_to_codes(user_input, Codes),
        Codes \= end_of_file
    ->  number_codes(N, Codes),
        n_queen_count(N, Count),
        writeln(Count)
    ;   true
    ).

n_queen_count(N, Count) :-
    count_positions(N, 0, 0, 0, 0, Count).

count_positions(N, R, Col, D1, D2, Count) :-
    (   R =:= N
    ->  Count = 1
    ;   count_columns(0, N, R, Col, D1, D2, 0, Count)
    ).

count_columns(C, N, R, Col, D1, D2, Acc0, Acc) :-
    (   C >= N
    ->  Acc = Acc0
    ;   B is 1 << C,
        D1B is 1 << (R + C),
        D2B is 1 << (R - C + N - 1),
        (   (Col /\ B) =:= 0,
            (D1 /\ D1B) =:= 0,
            (D2 /\ D2B) =:= 0
        ->  NewCol is Col \/ B,
            NewD1 is D1 \/ D1B,
            NewD2 is D2 \/ D2B,
            R1 is R + 1,
            count_positions(N, R1, NewCol, NewD1, NewD2, Sub),
            Acc1 is Acc0 + Sub
        ;   Acc1 = Acc0
        ),
        C1 is C + 1,
        count_columns(C1, N, R, Col, D1, D2, Acc1, Acc)
    ).