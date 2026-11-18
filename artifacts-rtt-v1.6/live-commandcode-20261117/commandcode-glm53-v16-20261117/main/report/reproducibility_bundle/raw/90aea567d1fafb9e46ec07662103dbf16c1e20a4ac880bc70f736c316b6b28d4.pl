:- module(main, [main/0]).
:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, NLine),
    read_line_to_string(user_input, ALine),
    number_string(N, NLine),
    split_string(ALine, " ", " ", Parts),
    maplist(number_string, A, Parts),
    length(A, N),
    A = [First|Rest],
    kadane(Rest, First, First, Best),
    write(Best), nl.

kadane([], _, Best, Best).
kadane([X|Xs], Cur, Best0, Best) :-
    Cur1 is max(X, Cur + X),
    Best1 is max(Best0, Cur1),
    kadane(Xs, Cur1, Best1, Best).