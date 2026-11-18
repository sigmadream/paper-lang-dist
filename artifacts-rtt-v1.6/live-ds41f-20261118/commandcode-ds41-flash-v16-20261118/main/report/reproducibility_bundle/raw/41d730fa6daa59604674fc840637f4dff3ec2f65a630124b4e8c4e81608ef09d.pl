:- use_module(library(lists)).

main :-
    read_all_codes(Codes),
    codes_to_ints(Codes, Ints),
    Ints = [N|ScoreTokens],
    length(Scores, N),
    append(Scores, _, ScoreTokens),
    solve(N, Scores, Ans),
    format('~d~n', [Ans]).

read_all_codes(Codes) :-
    read_codes(Codes).

read_codes(Codes) :-
    get_code(user_input, C),
    (   C =:= -1
    ->  Codes = []
    ;   Codes = [C|Rest],
        read_codes(Rest)
    ).

codes_to_ints(Codes, Ints) :-
    codes_to_ints(Codes, [], Ints).

codes_to_ints([], Acc, Ints) :-
    (   Acc = []
    ->  Ints = []
    ;   reverse(Acc, Rev),
        digits_value(Rev, N),
        Ints = [N]
    ).
codes_to_ints([C|Cs], Acc, Ints) :-
    C >= 48,
    C =< 57,
    !,
    codes_to_ints(Cs, [C|Acc], Ints).
codes_to_ints([_|Cs], Acc, Ints) :-
    (   Acc = []
    ->  codes_to_ints(Cs, [], Ints)
    ;   reverse(Acc, Rev),
        digits_value(Rev, N),
        Ints = [N|Rest],
        codes_to_ints(Cs, [], Rest)
    ).

digits_value(Digits, Value) :-
    digits_value(Digits, 0, Value).

digits_value([], V, V).
digits_value([D|Ds], Acc, V) :-
    Acc1 is Acc * 10 + (D - 48),
    digits_value(Ds, Acc1, V).

solve(N, Scores, Ans) :-
    N =:= 1,
    !,
    Scores = [S1|_],
    Ans = S1.
solve(N, Scores, Ans) :-
    N =:= 2,
    !,
    Scores = [S1, S2|_],
    Ans is S1 + S2.
solve(N, Scores, Ans) :-
    Scores = [S1, S2|_],
    A = 0,
    B = S1,
    C is S1 + S2,
    loop(3, N, Scores, A, B, C, Ans).

loop(I, N, Scores, A, B, C, Ans) :-
    (   I > N
    ->  Ans = C
    ;   nth1(I, Scores, Si),
        Iprev is I - 1,
        nth1(Iprev, Scores, Sprev),
        X is A + Sprev,
        (   B >= X
        ->  M = B
        ;   M = X
        ),
        D is M + Si,
        A1 = B,
        B1 = C,
        C1 = D,
        I2 is I + 1,
        loop(I2, N, Scores, A1, B1, C1, Ans)
    ).