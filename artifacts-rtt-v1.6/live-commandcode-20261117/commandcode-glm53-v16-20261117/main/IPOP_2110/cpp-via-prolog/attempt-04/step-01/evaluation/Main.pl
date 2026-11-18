:- use_module(library(readutil)).

read_all_numbers(Nums) :-
    read_line_to_codes(user_input, L),
    ( L == end_of_file -> Nums = []
    ; phrase(numbers(Nums0), L), read_all_numbers(Rest),
      append(Nums0, Rest, Nums)
    ).

numbers([N|T]) --> ws, number_codes_(N), !, numbers(T).
numbers([]) --> ws, [].
ws --> [C], { C == 32 ; C == 9 ; C == 13 }, !, ws.
ws --> [].

number_codes_(N) --> digits(D), { number_codes(N, D) }.
digits([D|T]) --> [D], { D >= 48, D =< 57 }, !, digits(T).
digits([]) --> [].

count_ok(Sorted, Mid, C) :-
    Sorted = [First|Rest],
    count_loop(Rest, First, Mid, 1, Count),
    Count >= C.

count_loop([], _, _, Count, Count).
count_loop([X|Xs], Prev, Mid, Acc, Count) :-
    ( X - Prev >= Mid ->
        Acc1 is Acc + 1,
        count_loop(Xs, X, Mid, Acc1, Count)
    ; count_loop(Xs, Prev, Mid, Acc, Count)
    ).

binary_search(Sorted, C, Lo, Hi, Ans0, Ans) :-
    ( Lo > Hi -> Ans = Ans0
    ; Mid is Lo + (Hi - Lo) // 2,
      ( count_ok(Sorted, Mid, C) ->
          Ans1 is Mid,
          Lo1 is Mid + 1,
          binary_search(Sorted, C, Lo1, Hi, Ans1, Ans)
      ; Hi1 is Mid - 1,
          binary_search(Sorted, C, Lo, Hi1, Ans0, Ans)
      )
    ).

main :-
    read_all_numbers(Nums),
    ( Nums == [] -> true
    ; Nums = [N, C|Coords],
      length(Coords, N),
      msort(Coords, Sorted),
      Sorted = [First|_],
      last(Sorted, Last),
      Hi is Last - First,
      binary_search(Sorted, C, 1, Hi, 0, Ans),
      format("~d~n", [Ans])
    ).