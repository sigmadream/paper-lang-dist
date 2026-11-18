main :-
    read_string(user_input, end_of_file, Input),
    split_string(Input, " \n\r\t", " \n\r\t", Tokens),
    Tokens = [NStr, CStr | HouseStrs],
    number_string(_N, NStr),
    number_string(C, CStr),
    maplist(number_string, Houses, HouseStrs),
    msort(Houses, Sorted),
    Sorted = [First | _],
    last(Sorted, Last),
    Max is Last - First,
    bin_search(1, Max, Sorted, C, 0, Ans),
    format("~w~n", [Ans]).

bin_search(L, R, _, _, Ans, Ans) :-
    L > R.
bin_search(L, R, Sorted, C, Best, Ans) :-
    L =< R,
    Mid is L + (R - L) // 2,
    count_fit(Sorted, Mid, Count),
    (   Count >= C ->
        Best1 = Mid,
        L1 is Mid + 1,
        bin_search(L1, R, Sorted, C, Best1, Ans)
    ;   R1 is Mid - 1,
        bin_search(L, R1, Sorted, C, Best, Ans)
    ).

count_fit([First | Rest], D, Count) :-
    count_fit(Rest, D, 1, First, Count).

count_fit([], _, Count, _, Count).
count_fit([X | Xs], D, Count0, Prev, Count) :-
    (   X - Prev >= D ->
        Count1 is Count0 + 1,
        count_fit(Xs, D, Count1, X, Count)
    ;   count_fit(Xs, D, Count0, Prev, Count)
    ).