:- use_module(library(readutil)).

main :-
    current_input(In),
    read_all_lines(In, Lines),
    atomics_to_string(Lines, " ", All),
    split_string(All, " \t\r\n", " \t\r\n", Tokens),
    ( Tokens == [] ->
        true
    ; maplist(token_to_int, Tokens, Nums),
      Nums = [N|Rest],
      ( N > 0 ->
          take(N, Rest, Values),
          Values = [First|Tail],
          kadane(Tail, First, First, Best),
          format("~w~n", [Best])
      ; true
      )
    ),
    halt.

read_all_lines(In, Lines) :-
    read_line_to_string(In, Line),
    ( Line == end_of_file ->
        Lines = []
    ; Lines = [Line|Rest],
      read_all_lines(In, Rest)
    ).

token_to_int(Str, Num) :-
    string_codes(Str, Codes),
    number_codes(Num, Codes).

take(0, _, []) :- !.
take(N, [X|Xs], [X|Ys]) :-
    N > 0,
    N1 is N - 1,
    take(N1, Xs, Ys).

kadane([], _, Best, Best).
kadane([X|Xs], Cur, Best0, Best) :-
    Sum is Cur + X,
    ( X > Sum -> Cur1 = X ; Cur1 = Sum ),
    ( Cur1 > Best0 -> Best1 = Cur1 ; Best1 = Best0 ),
    kadane(Xs, Cur1, Best1, Best).