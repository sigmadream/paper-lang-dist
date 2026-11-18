main :-
    ( catch(read(N), _, fail),
      integer(N),
      N > 0 ->
        read_numbers(N, Nums),
        Nums = [First|Rest],
        max_sub(Rest, First, First, Best),
        write(Best), nl
    ; true
    ).

read_numbers(0, []) :- !.
read_numbers(N, [X|Xs]) :-
    N1 is N - 1,
    read(X),
    read_numbers(N1, Xs).

max_sub([], _, Best, Best).
max_sub([Y|Ys], Cur0, Best0, Best) :-
    CurSum is Cur0 + Y,
    ( Y > CurSum -> Cur1 = Y ; Cur1 = CurSum ),
    ( Cur1 > Best0 -> Best1 = Cur1 ; Best1 = Best0 ),
    max_sub(Ys, Cur1, Best1, Best).