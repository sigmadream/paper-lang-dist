:- use_module(library(lists)).

main :-
    read_all_codes(Codes),
    tokens(Codes, Tokens),
    Tokens = [N|AllScores],
    length(Scores, N),
    append(Scores, _, AllScores),
    solve(N, Scores, Ans),
    format('~w~n', [Ans]).

read_all_codes(Codes) :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        Codes = []
    ; string_codes(Line, LineCodes),
      read_all_codes(Rest),
      append(LineCodes, [10|Rest], Codes)
    ).

tokens(Codes, Tokens) :-
    skip_ws(Codes, Rest),
    ( Rest = [] ->
        Tokens = []
    ; take_token(Rest, TokenCodes, Rest1),
      number_codes(Number, TokenCodes),
      Tokens = [Number|More],
      tokens(Rest1, More)
    ).

skip_ws([C|Cs], Rest) :-
    is_ws(C), !,
    skip_ws(Cs, Rest).
skip_ws(Cs, Cs).

take_token([C|Cs], [C|Token], Rest) :-
    \+ is_ws(C), !,
    take_token(Cs, Token, Rest).
take_token(Cs, [], Cs).

is_ws(32).
is_ws(9).
is_ws(10).
is_ws(13).

solve(N, Scores, Ans) :-
    ( N =:= 1 ->
        Scores = [S1|_],
        Ans = S1
    ; N =:= 2 ->
        Scores = [S1,S2|_],
        Ans is S1 + S2
    ; build_dp(N, Scores, DP),
      nth1(N, DP, Ans)
    ).

build_dp(N, Scores, DP) :-
    Scores = [S1,S2|_],
    D1 = S1,
    D2 is S1 + S2,
    dp_loop(3, N, Scores, 0, D1, D2, [D2,D1], RevDP),
    reverse(RevDP, DP).

dp_loop(I, N, Scores, DPrev3, DPrev2, DPrev1, Acc, RevDP) :-
    ( I > N ->
        RevDP = Acc
    ; nth1(I, Scores, Si),
      Im1 is I - 1,
      nth1(Im1, Scores, Sim1),
      ( DPrev2 >= DPrev3 + Sim1 ->
          Best = DPrev2
      ; Best is DPrev3 + Sim1
      ),
      Di is Best + Si,
      I1 is I + 1,
      dp_loop(I1, N, Scores, DPrev2, DPrev1, Di, [Di|Acc], RevDP)
    ).