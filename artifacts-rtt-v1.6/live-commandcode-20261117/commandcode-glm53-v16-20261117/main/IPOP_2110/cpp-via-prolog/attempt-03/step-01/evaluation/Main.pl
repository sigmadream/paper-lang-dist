main :-
    read_line_to_codes(user_input, L1),
    ( L1 == end_of_file -> true
    ; parse_two(L1, N, C, Rest1),
      read_all_coords(N, Coords0, Rest1),
      msort(Coords0, Coords),
      Coords = [First|_],
      last(Coords, Last),
      MaxD is Last - First,
      binary_search(1, MaxD, Coords, C, 0, Ans),
      format("~d~n", [Ans])
    ).

parse_two(L, N, C, Rest) :-
    number_codes(N, D1, R1),
    skip_ws(R1, R2),
    number_codes(C, D2, R3),
    skip_ws(R3, Rest).

skip_ws([H|T], T) :- H >= 48, !.
skip_ws([], []) :- !.
skip_ws([32,10|T], T) :- !.
skip_ws([10|T], T) :- !.
skip_ws([32|T], R) :- !, skip_ws(T, R).
skip_ws([_|T], R) :- skip_ws(T, R).

read_all_coords(0, [], Rest) :- !.
read_all_coords(N, [X|Xs], Rest) :-
    number_codes(X, _, Rest, Rest2),
    skip_ws(Rest2, Rest3),
    N1 is N - 1,
    read_all_coords(N1, Xs, Rest3).

number_codes(N) --> num_codes(Ds), {number_codes(N, Ds)}.
num_codes([D|Ds]) --> digit(D), num_codes_rest(Ds).
num_codes_rest([D|Ds]) --> digit(D), !, num_codes_rest(Ds).
num_codes_rest([]) --> [].
digit(D) --> [C], {C >= 48, C =< 57, D is C - 48}.

last([X], X) :- !.
last([_|T], X) :- last(T, X).

binary_search(Left, Right, _, _, Ans, Ans) :- Left > Right, !.
binary_search(Left, Right, Coords, C, _, Ans) :-
    Mid is Left + (Right - Left) // 2,
    Coords = [First|_],
    count_placed(Coords, Mid, 1, First, Count),
    ( Count >= C ->
        Ans0 = Mid,
        NewLeft is Mid + 1,
        binary_search(NewLeft, Right, Coords, C, Ans0, Ans)
    ;
        NewRight is Mid - 1,
        binary_search(Left, NewRight, Coords, C, _, Ans)
    ).

count_placed([], _, Count, _, Count).
count_placed([X|Xs], Mid, Count, Prev, Total) :-
    ( X - Prev >= Mid ->
        Count1 is Count + 1,
        Prev1 = X
    ;
        Count1 = Count,
        Prev1 = Prev
    ),
    count_placed(Xs, Mid, Count1, Prev1, Total).