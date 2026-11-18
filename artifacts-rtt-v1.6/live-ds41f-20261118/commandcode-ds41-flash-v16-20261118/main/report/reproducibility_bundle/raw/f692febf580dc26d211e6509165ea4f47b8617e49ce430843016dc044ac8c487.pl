% Unique Paths - LC_0062
% Reads M and N from standard input and prints the number of unique paths.

main :-
    read_line_to_codes(user_input, Codes),
    (   Codes == end_of_file
    ->  true
    ;   read_int_codes(Codes, Nums),
        Nums = [M, N | _],
        paths(M, N, Ans),
        writeln(Ans)
    ).

read_int_codes(Codes, Nums) :-
    skip_ws(Codes, Rest),
    (   Rest == []
    ->  Nums = []
    ;   take_digits(Rest, Digits, Rest2),
        number_codes(N, Digits),
        Nums = [N | Nums2],
        read_int_codes(Rest2, Nums2)
    ).

skip_ws([C | Cs], Rest) :-
    ws(C),
    !,
    skip_ws(Cs, Rest).
skip_ws(Rest, Rest).

ws(32).
ws(9).
ws(10).
ws(13).

take_digits([C | Cs], [C | Ds], Rest) :-
    C >= 48,
    C =< 57,
    !,
    take_digits(Cs, Ds, Rest).
take_digits(Rest, [], Rest).

paths(M, N, Ans) :-
    length(Row, N),
    maplist(=(1), Row),
    Rows is M - 1,
    apply_rows(Rows, Row, FinalRow),
    last(FinalRow, Ans).

apply_rows(0, Row, Row).
apply_rows(K, Row, Final) :-
    K > 0,
    update_row(Row, NewRow),
    K1 is K - 1,
    apply_rows(K1, NewRow, Final).

update_row([_ | OldTail], NewRow) :-
    NewRow = [1 | NewTail],
    upd_tail(OldTail, 1, NewTail).

upd_tail([], _, []).
upd_tail([O | Os], Prev, [V | Vs]) :-
    V is Prev + O,
    upd_tail(Os, V, Vs).