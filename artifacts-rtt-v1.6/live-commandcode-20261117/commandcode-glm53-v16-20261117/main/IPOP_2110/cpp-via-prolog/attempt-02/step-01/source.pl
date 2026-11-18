:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, string).

read_ints(Ints) :-
    read_line_to_codes(user_input, Cs),
    ( Cs == end_of_file -> Ints = []
    ; Cs == [] -> Ints = []
    ; atom_codes(A, Cs), split_string(A, " \t\r\n", " \t\r\n", Parts),
      maplist(number_string, Ints, Parts)
    ).

read_all(All) :-
    read_line_to_codes(user_input, Cs),
    ( Cs == end_of_file -> All = []
    ; Cs == [] -> All = []
    ; atom_codes(A, Cs), split_string(A, " \t\r\n", " \t\r\n", Parts),
      maplist(number_string, Nums, Parts),
      append(Nums, Rest, All0), read_all(Rest), All = All0
    ).

main :-
    catch(
        ( read_all(Data),
          Data \== []
        ),
        _,
        Data = []
    ),
    ( var(Data) -> Data = [] ; true ),
    ( Data == [] -> true
    ; Data = [N, C|Coords],
        msort(Coords, Sorted),
        length(Coords, N),
        ( N =:= 0 -> Ans = 0
        ; Sorted = [First|_],
          reverse(Sorted, [Last|_]),
          Range is Last - First,
          binary_search(1, Range, Sorted, C, 0, Ans)
        ),
        format("~d~n", [Ans])
    ).

binary_search(Left, Right, _, _, Acc, Acc) :- Left > Right, !.
binary_search(Left, Right, Sorted, C, _, Ans) :-
    Left =< Right,
    Mid is Left + (Right - Left) // 2,
    count_installed(Sorted, Mid, Count),
    ( Count >= C ->
        NextAcc is Mid,
        NextLeft is Mid + 1,
        binary_search(NextLeft, Right, Sorted, C, NextAcc, Ans)
    ;
        NextRight is Mid - 1,
        binary_search(Left, NextRight, Sorted, C, _, Ans)
    ).

count_installed([First|Rest], Mid, Count) :-
    count_loop(Rest, First, Mid, 1, Count).

count_loop([], _, _, Count, Count).
count_loop([X|Xs], Prev, Mid, Acc, Count) :-
    ( X - Prev >= Mid ->
        NewAcc is Acc + 1,
        count_loop(Xs, X, Mid, NewAcc, Count)
    ;
        count_loop(Xs, Prev, Mid, Acc, Count)
    ).