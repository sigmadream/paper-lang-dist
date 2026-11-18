:- module(main, [main/0]).
:- use_module(library(readutil)).

main :-
    read_string(user_input, end_of_file, Input),
    split_string(Input, " \t\r\n", " \t\r\n", Tokens),
    Tokens = [NStr | Rest],
    number_string(N, NStr),
    take_numbers(N, Rest, Values),
    max_subarray(Values, Best),
    format("~w~n", [Best]).

take_numbers(0, _, []) :- !.
take_numbers(N, [S | Ss], [V | Vs]) :-
    N > 0,
    number_string(V, S),
    N1 is N - 1,
    take_numbers(N1, Ss, Vs).

max_subarray([X | Xs], Best) :-
    max_subarray_loop(Xs, X, X, Best).

max_subarray_loop([], _Cur, Best, Best).
max_subarray_loop([X | Xs], Cur, Best0, Best) :-
    T is Cur + X,
    ( X >= T -> Cur1 = X ; Cur1 = T ),
    ( Cur1 >= Best0 -> Best1 = Cur1 ; Best1 = Best0 ),
    max_subarray_loop(Xs, Cur1, Best1, Best).