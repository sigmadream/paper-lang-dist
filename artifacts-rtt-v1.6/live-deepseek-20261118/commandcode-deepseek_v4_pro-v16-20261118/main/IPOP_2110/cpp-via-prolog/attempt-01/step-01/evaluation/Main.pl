:- use_module(library(dcg/basics)).

main :-
    read_line_to_codes(user_input, FirstLine),
    phrase((integer(N), whites, integer(C), whites, eos), FirstLine),
    read_coordinates(N, Coords),
    solve(C, Coords, Ans),
    format("~d~n", [Ans]).

read_coordinates(0, []) :- !.
read_coordinates(Count, [X|Xs]) :-
    read_line_to_codes(user_input, Line),
    Line \= end_of_file,
    phrase((integer(X), whites, eos), Line),
    Count1 is Count - 1,
    read_coordinates(Count1, Xs).

solve(C, Coords, Ans) :-
    sort(Coords, Sorted),
    Sorted = [First|_],
    last(Sorted, Last),
    Right is Last - First,
    search(1, Right, Sorted, C, 0, Ans).

search(Left, Right, A, C, Ans0, Ans) :-
    ( Left =< Right ->
        Mid is Left + (Right - Left) // 2,
        ( can_place(A, Mid, C) ->
            Left1 is Mid + 1,
            search(Left1, Right, A, C, Mid, Ans)
        ;
            Right1 is Mid - 1,
            search(Left, Right1, A, C, Ans0, Ans)
        )
    ;
        Ans = Ans0
    ).

can_place([H|T], Mid, C) :-
    can_place(T, Mid, H, 1, C).

can_place([], _, _, Count, C) :-
    Count >= C.

can_place([X|T], Mid, Prev, Count0, C) :-
    ( X - Prev >= Mid ->
        Count1 is Count0 + 1,
        Prev1 = X
    ;
        Count1 = Count0,
        Prev1 = Prev
    ),
    ( Count1 >= C ->
        true
    ;
        can_place(T, Mid, Prev1, Count1, C)
    ).