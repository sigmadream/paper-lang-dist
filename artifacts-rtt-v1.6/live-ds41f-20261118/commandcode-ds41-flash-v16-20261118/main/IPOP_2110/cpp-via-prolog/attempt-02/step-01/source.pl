prepend(X, Acc, [X|Acc]).

read_tokens(Rev, Tokens) :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        reverse(Rev, Tokens)
    ; split_string(Line, " \t\r\n", " \t\r\n", Parts),
      foldl(prepend, Parts, Rev, NewRev),
      read_tokens(NewRev, Tokens)
    ).

can_place([First|Rest], D, C) :-
    can_place_rest(Rest, D, First, 1, C).

can_place_rest(_, _, _, Count, C) :-
    Count >= C, !.
can_place_rest([], _, _, Count, C) :-
    Count >= C.
can_place_rest([X|Xs], D, Prev, Count0, C) :-
    ( X - Prev >= D ->
        Count1 is Count0 + 1,
        can_place_rest(Xs, D, X, Count1, C)
    ; can_place_rest(Xs, D, Prev, Count0, C)
    ).

bs(Lo, Hi, A, C, Ans, Result) :-
    ( Lo =< Hi ->
        Mid is Lo + ((Hi - Lo) // 2),
        ( can_place(A, Mid, C) ->
            Ans1 = Mid,
            Lo1 is Mid + 1,
            Hi1 = Hi
        ; Ans1 = Ans,
            Lo1 = Lo,
            Hi1 is Mid - 1
        ),
        bs(Lo1, Hi1, A, C, Ans1, Result)
    ; Result = Ans
    ).

main :-
    read_tokens([], Tokens),
    ( Tokens = [NStr, CStr | CoordStrs] ->
        number_string(N, NStr),
        number_string(C, CStr),
        length(CoordStrs, N),
        maplist(number_string, Coords, CoordStrs),
        msort(Coords, Sorted),
        Sorted = [First|_],
        last(Sorted, Last),
        Hi is Last - First,
        bs(1, Hi, Sorted, C, 0, Ans),
        writeln(Ans)
    ; true
    ).