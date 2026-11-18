read_all_tokens(Tokens) :-
    read_lines([], LinesRev),
    reverse(LinesRev, Lines),
    flatten_parts(Lines, Tokens).

read_lines(Acc, Lines) :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        Lines = Acc
    ; split_string(Line, " \t\r\n", " \t\r\n", Parts),
      read_lines([Parts|Acc], Lines)
    ).

flatten_parts([], []).
flatten_parts([Parts|Rest], All) :-
    append(Parts, Tail, All),
    flatten_parts(Rest, Tail).

tokens_to_numbers([], []).
tokens_to_numbers([S|Ss], Ns) :-
    ( S == "" ->
        tokens_to_numbers(Ss, Ns)
    ; atom_number(S, N),
      Ns = [N|Rest],
      tokens_to_numbers(Ss, Rest)
    ).

take_first(0, _, []) :- !.
take_first(N, [H|T], [H|R]) :-
    N > 0,
    N1 is N - 1,
    take_first(N1, T, R).

max_subarray([], 0).
max_subarray([First|Rest], Best) :-
    max_subarray_rest(Rest, First, First, Best).

max_subarray_rest([], _, Best, Best).
max_subarray_rest([X|Xs], Cur, Best, Final) :-
    CurPlusX is Cur + X,
    ( X > CurPlusX -> Cur1 = X ; Cur1 = CurPlusX ),
    ( Best > Cur1 -> Best1 = Best ; Best1 = Cur1 ),
    max_subarray_rest(Xs, Cur1, Best1, Final).

main :-
    read_all_tokens(Parts),
    tokens_to_numbers(Parts, Nums),
    Nums = [N|Rest],
    take_first(N, Rest, Values),
    max_subarray(Values, Best),
    writeln(Best).