read_all_codes(Codes) :-
    current_input(S),
    read_codes(S, Codes).

read_codes(S, [C|Cs]) :-
    get_code(S, C),
    C =\= -1,
    !,
    read_codes(S, Cs).
read_codes(_, []).

parse_ints([], []).
parse_ints([C|Cs], Ints) :-
    C >= 48,
    C =< 57,
    !,
    Num0 is C - 48,
    parse_number(Cs, Num0, Num, Rest),
    Ints = [Num|RestInts],
    parse_ints(Rest, RestInts).
parse_ints([_|Cs], Ints) :-
    parse_ints(Cs, Ints).

parse_number([C|Cs], Acc, Num, Rest) :-
    C >= 48,
    C =< 57,
    !,
    Acc1 is Acc * 10 + (C - 48),
    parse_number(Cs, Acc1, Num, Rest).
parse_number(Rest, Acc, Acc, Rest).

take_edges(0, _, []).
take_edges(M, [A,B|T], [A-B|Es]) :-
    M > 0,
    M1 is M - 1,
    take_edges(M1, T, Es).

count_valid([], _, Acc, Acc).
count_valid([H|T], D1, Acc, Res) :-
    ( H =:= 1 ; memberchk(H, D1) ) ->
        count_valid(T, D1, Acc, Res)
    ;
        Acc1 is Acc + 1,
        count_valid(T, D1, Acc1, Res).

main :-
    read_all_codes(Codes),
    parse_ints(Codes, Ints),
    ( Ints = [_N, M | Rest] ->
        take_edges(M, Rest, Edges),
        findall(U,
                ( member(A-B, Edges),
                  ( (A =:= 1, U = B) ; (B =:= 1, U = A) )
                ),
                L1Raw),
        sort(L1Raw, L1),
        findall(U,
                ( member(V, L1),
                  member(A-B, Edges),
                  ( (A =:= V, U = B) ; (B =:= V, U = A) )
                ),
                L2Raw),
        sort(L2Raw, L2),
        count_valid(L2, L1, 0, C2),
        length(L1, C1),
        Ans is C1 + C2,
        write(Ans), nl
    ; true
    ).