main :-
    read_string(current_input, end_of_file, Input),
    split_string(Input, " \n\r\t", " \n\r\t", Parts),
    parse_ints(Parts, Nums),
    ( Nums = [_N, C | Coords] ->
        msort(Coords, Sorted),
        Sorted = [First | _],
        last(Sorted, Last),
        Hi is Last - First,
        Need is C - 1,
        binary_search(1, Hi, Sorted, Need, 0, Ans),
        format("~w~n", [Ans])
    ; true
    ).

parse_ints([], []).
parse_ints([P | Ps], [N | Ns]) :-
    number_string(N, P),
    parse_ints(Ps, Ns).

binary_search(Lo, Hi, Sorted, Need, Ans0, Ans) :-
    ( Lo > Hi ->
        Ans = Ans0
    ; Mid is Lo + (Hi - Lo) // 2,
      ( can_place(Sorted, Mid, Need) ->
          Ans1 = Mid,
          Lo1 is Mid + 1,
          binary_search(Lo1, Hi, Sorted, Need, Ans1, Ans)
      ; Hi1 is Mid - 1,
        binary_search(Lo, Hi1, Sorted, Need, Ans0, Ans)
      )
    ).

can_place([First | Rest], D, Need) :-
    place(Rest, D, First, Need).

place([], _, _, Need) :-
    Need =< 0.
place([H | T], D, Prev, Need) :-
    ( H - Prev >= D ->
        Need1 is Need - 1,
        ( Need1 =< 0 ->
            true
        ; place(T, D, H, Need1)
        )
    ; place(T, D, Prev, Need)
    ).