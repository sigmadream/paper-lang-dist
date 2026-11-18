main :-
    read_line_to_codes(user_input, Codes),
    ( Codes == end_of_file ->
        true
    ; parse_ints(Codes, Ints),
      ( Ints = [M, N | _] ->
          solve(M, N, Ans),
          format("~w~n", [Ans])
      ; true
      )
    ).

parse_ints([], []).
parse_ints([C|Cs], Ints) :-
    is_space(C), !,
    parse_ints(Cs, Ints).
parse_ints(Cs, [N|Ns]) :-
    parse_number(Cs, Digits, Rest),
    number_codes(N, Digits),
    parse_ints(Rest, Ns).

parse_number([C|Cs], [C|Ds], Rest) :-
    code_type(C, digit), !,
    parse_number(Cs, Ds, Rest).
parse_number(Rest, [], Rest).

is_space(32).
is_space(9).
is_space(10).
is_space(13).

solve(M, N, Ans) :-
    fill_ones(N, Row),
    M1 is M - 1,
    iterate_rows(1, M1, Row, FinalRow),
    Idx is N - 1,
    nth0(Idx, FinalRow, Ans).

fill_ones(0, []) :- !.
fill_ones(N, [1|T]) :-
    N > 0,
    N1 is N - 1,
    fill_ones(N1, T).

iterate_rows(I, Max, Row, Final) :-
    ( I > Max ->
        Final = Row
    ; update_row(Row, NewRow),
      I1 is I + 1,
      iterate_rows(I1, Max, NewRow, Final)
    ).

update_row([First|Rest], [First|NewRest]) :-
    update_rest(Rest, First, NewRest).

update_rest([], _, []).
update_rest([Old|Olds], Prev, [New|News]) :-
    New is Old + Prev,
    update_rest(Olds, New, News).