:- use_module(library(readutil)).

main :-
    read_tokens([], RevTokens),
    reverse(RevTokens, Tokens),
    Tokens = [_NStr, CStr | CoordStr],
    number_string(C, CStr),
    to_ints(CoordStr, Coords),
    msort(Coords, Sorted),
    solve(Sorted, C, Ans),
    format('~w~n', [Ans]).

read_tokens(Acc, TokensRev) :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  TokensRev = Acc
    ;   split_string(Line, " \t\r", " \t\r", Parts),
        append_rev(Parts, Acc, Acc1),
        read_tokens(Acc1, TokensRev)
    ).

append_rev([], Acc, Acc).
append_rev([P|Ps], Acc, Out) :-
    append_rev(Ps, [P|Acc], Out).

to_ints([], []).
to_ints([S|Ss], [N|Ns]) :-
    number_string(N, S),
    to_ints(Ss, Ns).

solve(Sorted, C, Ans) :-
    Sorted = [First|_],
    list_last(Sorted, Last),
    MaxDist is Last - First,
    binary_search(1, MaxDist, Sorted, C, 0, Ans).

list_last([X], X) :- !.
list_last([_|T], X) :-
    list_last(T, X).

binary_search(Left, Right, Sorted, C, CurrentAns, Ans) :-
    (   Left > Right
    ->  Ans = CurrentAns
    ;   Mid is Left + (Right - Left) // 2,
        count_possible(Sorted, Mid, Count),
        (   Count >= C
        ->  Left1 is Mid + 1,
            binary_search(Left1, Right, Sorted, C, Mid, Ans)
        ;   Right1 is Mid - 1,
            binary_search(Left, Right1, Sorted, C, CurrentAns, Ans)
        )
    ).

count_possible([First|Rest], Mid, Count) :-
    count_rest(Rest, Mid, First, 1, Count).

count_rest([], _, _, Acc, Acc).
count_rest([H|T], Mid, Prev, Acc, Count) :-
    (   H - Prev >= Mid
    ->  Acc1 is Acc + 1,
        Prev1 = H
    ;   Acc1 = Acc,
        Prev1 = Prev
    ),
    count_rest(T, Mid, Prev1, Acc1, Count).