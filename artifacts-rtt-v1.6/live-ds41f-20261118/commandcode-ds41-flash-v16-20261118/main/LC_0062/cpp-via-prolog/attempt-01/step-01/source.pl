main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", RawParts),
    exclude(nonempty, RawParts, Parts),
    Parts = [MStr, NStr | _],
    number_string(M, MStr),
    number_string(N, NStr),
    length(Dp0, N),
    maplist(=(1), Dp0),
    Steps is M - 1,
    iterate_rows(Steps, Dp0, Dp),
    last(Dp, Answer),
    write(Answer), nl.

nonempty(S) :-
    S \= "".

iterate_rows(0, Dp, Dp).
iterate_rows(K, Dp, Result) :-
    K > 0,
    next_row(Dp, Dp1),
    K1 is K - 1,
    iterate_rows(K1, Dp1, Result).

next_row([First|Rest], [First|NewRest]) :-
    next_rest(Rest, First, NewRest).

next_rest([], _, []).
next_rest([Old|Olds], Prev, [New|News]) :-
    New is Old + Prev,
    next_rest(Olds, New, News).