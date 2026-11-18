:- module(main, [main/0]).
:- use_module(library(readutil)).
:- use_module(library(apply)).

main :-
    catch(run, _, true).

run :-
    read_line_to_codes(user_input, L1),
    (L1 == end_of_file -> true ;
        phrase(nums(L1), [N, C]),
        read_all(N, Xs0),
        msort(Xs0, Xs),
        Xs = [First|_],
        last(Xs, Last),
        Hi0 is Last - First,
        binary_search(1, Hi0, Xs, C, 0, Ans),
        format("~d~n", [Ans])).

read_all(0, []) :- !.
read_all(N, [X|T]) :-
    read_line_to_codes(user_input, L),
    (L == end_of_file -> T = [] ;
        phrase(nums(L), [X|Rest]),
        length([X|Rest], K),
        N2 is N - K,
        read_all(N2, T)).

nums([]) --> [].
nums([H|T]) -->
    {code_type(H, space)}, !, nums(T).
nums([H|T]) -->
        {code_type(H, digit)},
        number_codes_(T, [H], N),
        {N >= 0},
        [N],
        nums(T).

number_codes_([H|T], Acc, N) -->
    {code_type(H, digit)}, !,
    number_codes_(T, [H|Acc], N).
number_codes_(Rest, Acc, N) -->
    {reverse(Acc, Ds), number_codes(N, Ds)},
    Rest.

binary_search(Lo, Hi, _, _, Ans, Ans) :- Lo > Hi, !.
binary_search(Lo, Hi, Xs, C, _, Ans) :-
    Mid is Lo + (Hi - Lo) // 2,
    count_placed(Xs, Mid, Count),
    (Count >= C ->
        Lo2 is Mid + 1,
        binary_search(Lo2, Hi, Xs, C, Mid, Ans)
    ;
        Hi2 is Mid - 1,
        binary_search(Lo, Hi2, Xs, C, _, Ans)
    ).

count_placed([First|Rest], Mid, Count) :-
    count_loop(Rest, First, Mid, 1, Count).

count_loop([], _, _, C, C).
count_loop([X|T], Prev, Mid, Acc, Count) :-
    D is X - Prev,
    (D >= Mid ->
        Acc1 is Acc + 1,
        count_loop(T, X, Mid, Acc1, Count)
    ;
        count_loop(T, Prev, Mid, Acc, Count)
    ).