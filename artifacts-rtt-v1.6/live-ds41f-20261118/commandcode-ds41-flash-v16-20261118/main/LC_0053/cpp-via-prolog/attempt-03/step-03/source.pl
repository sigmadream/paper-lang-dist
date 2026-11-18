read_all_lines(Lines) :-
    read_line_to_string(user_input, L),
    ( L == end_of_file ->
        Lines = []
    ;
        Lines = [L|Rest],
        read_all_lines(Rest)
    ).

max_subarray([], 0).
max_subarray([X|Xs], Best) :-
    max_subarray_(Xs, X, X, Best).

max_subarray_([], _, Best, Best).
max_subarray_([X|Xs], Cur, Best, Result) :-
    Sum is Cur + X,
    ( X > Sum -> Cur1 = X ; Cur1 = Sum ),
    ( Cur1 > Best -> Best1 = Cur1 ; Best1 = Best ),
    max_subarray_(Xs, Cur1, Best1, Result).

main :-
    read_all_lines(Lines),
    atomic_list_concat(Lines, ' ', All),
    split_string(All, " \t\r\n", " \t\r\n", Tokens),
    Tokens = [NStr|NumStrs],
    number_string(N, NStr),
    length(NumStrs, N),
    maplist(number_string, Nums, NumStrs),
    max_subarray(Nums, Best),
    format("~w~n", [Best]).