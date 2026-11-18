main :-
    read_string(user_input, "", "", _, Input),
    split_string(Input, " \n\r\t", " ", Tokens0),
    delete(Tokens0, "", Tokens),
    maplist(number_string, Nums, Tokens),
    Nums = [N|Scores],
    solve(N, Scores, Answer),
    writeln(Answer).

solve(N, Scores, Answer) :-
    ( N =:= 1 ->
        Scores = [S1],
        Answer = S1
    ; N =:= 2 ->
        Scores = [S1, S2],
        Answer is S1 + S2
    ; Scores = [S1, S2 | Rest],
        DPrev3 = 0,
        DPrev2 = S1,
        DPrev1 is S1 + S2,
        loop(Rest, S2, DPrev3, DPrev2, DPrev1, Answer)
    ).

loop([], _, _, _, DPrev1, Answer) :-
    Answer = DPrev1.
loop([Cur|Rest], PrevScore, DPrev3, DPrev2, DPrev1, Answer) :-
    Best is max(DPrev2, DPrev3 + PrevScore),
    Di is Best + Cur,
    loop(Rest, Cur, DPrev2, DPrev1, Di, Answer).