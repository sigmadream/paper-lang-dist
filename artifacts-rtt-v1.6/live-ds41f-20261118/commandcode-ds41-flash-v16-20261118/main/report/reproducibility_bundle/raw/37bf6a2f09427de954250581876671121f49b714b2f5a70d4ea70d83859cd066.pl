:- use_module(library(readutil)).

main :-
    read_numbers([], RevNums),
    reverse(RevNums, Nums),
    Nums = [N, C | Rest],
    take_n(N, Rest, Houses),
    sort(Houses, Sorted),
    Sorted = [First | _],
    last(Sorted, Last),
    MaxDist is Last - First,
    binary_search(1, MaxDist, Sorted, C, 0, Answer),
    write(Answer), nl.

read_numbers(Acc, Nums) :-
    read_line_to_codes(user_input, Codes),
    (   Codes == end_of_file ->
        reverse(Acc, Nums)
    ;   split_ws(Codes, Tokens),
        maplist(code_to_int, Tokens, Ns),
        reverse(Ns, NsRev),
        append(NsRev, Acc, Acc1),
        read_numbers(Acc1, Nums)
    ).

code_to_int(Codes, N) :-
    number_codes(N, Codes).

split_ws([], []).
split_ws([C | Cs], Tokens) :-
    is_ws(C), !,
    split_ws(Cs, Tokens).
split_ws(Cs, [Token | Rest]) :-
    take_token(Cs, Token, Rest0),
    split_ws(Rest0, Rest).

take_token([], [], []).
take_token([C | Cs], [], [C | Cs]) :-
    is_ws(C), !.
take_token([C | Cs], [C | Token], Rest) :-
    take_token(Cs, Token, Rest).

is_ws(C) :-
    (   C =:= 32
    ;   C =:= 9
    ;   C =:= 10
    ;   C =:= 13
    ).

take_n(0, _, []).
take_n(N, [X | Xs], [X | Ys]) :-
    N > 0,
    N1 is N - 1,
    take_n(N1, Xs, Ys).

can_place([First | Rest], C, Dist) :-
    can_place_loop(Rest, First, 1, C, Dist).

can_place_loop(_, _, Count, C, _) :-
    Count >= C, !.
can_place_loop([H | T], Prev, Count, C, Dist) :-
    (   H - Prev >= Dist ->
        Count1 is Count + 1,
        can_place_loop(T, H, Count1, C, Dist)
    ;   can_place_loop(T, Prev, Count, C, Dist)
    ).
can_place_loop([], _, Count, C, _) :-
    Count >= C.

binary_search(L, R, _, _, Best, Best) :-
    L > R, !.
binary_search(L, R, Sorted, C, Best, Answer) :-
    Mid is L + (R - L) // 2,
    (   can_place(Sorted, C, Mid) ->
        Best1 = Mid,
        L1 is Mid + 1,
        binary_search(L1, R, Sorted, C, Best1, Answer)
    ;   R1 is Mid - 1,
        binary_search(L, R1, Sorted, C, Best, Answer)
    ).