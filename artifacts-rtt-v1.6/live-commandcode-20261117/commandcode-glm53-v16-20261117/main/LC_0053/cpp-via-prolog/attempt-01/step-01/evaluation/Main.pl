:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, string).

read_ints(N, Ints) :-
    ( N =:= 0 -> Ints = []
    ; read_int(X), N1 is N-1, read_ints(N1, Rest), Ints = [X|Rest]
    ).

read_int(X) :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file -> X = 0
    ; split_string(Line, " ", " \t\r\n", Parts),
      member(P, Parts), number_string(X, P), !
    ; X = 0
    ).

max_subarray([H|T], Best) :-
    H =\= 0 -> % placeholder, replaced below
    fail.
max_subarray([First|Rest], Best) :-
    ( First =:= 0 -> C0 = 0 ; C0 = First ),
    max_sub(Best, Rest, First, First).

max_sub(Best, [], _, Best).
max_sub(Best, [X|T], Cur, B) :-
    ( X > Cur + X -> NewCur = X ; NewCur is Cur + X ),
    ( NewCur > B -> NewB = NewCur ; NewB = B ),
    max_sub(Best, T, NewCur, NewB).

main :-
    read_int(N),
    read_ints(N, As),
    ( As == [] -> Best = 0
    ; max_subarray(As, Best)
    ),
    format("~d~n", [Best]),
    halt.