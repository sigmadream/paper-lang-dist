read_line_codes(Codes) :-
    read_line_codes_acc([], Rev),
    reverse(Rev, Codes).

read_line_codes_acc(Acc, Codes) :-
    get_code(C),
    (   C =:= -1
    ->  Codes = Acc
    ;   C =:= 10
    ->  Codes = Acc
    ;   C =:= 13
    ->  read_line_codes_acc(Acc, Codes)
    ;   read_line_codes_acc([C|Acc], Codes)
    ).

main :-
    read_line_codes(S),
    read_line_codes(T),
    msort(S, SS),
    msort(T, TT),
    (   SS == TT
    ->  Result = 1
    ;   Result = 0
    ),
    format("~w~n", [Result]).