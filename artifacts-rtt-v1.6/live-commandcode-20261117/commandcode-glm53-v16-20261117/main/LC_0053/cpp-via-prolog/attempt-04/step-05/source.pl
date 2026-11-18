:- module(main, [main/0]).
:- use_module(library(charsio)).

read_ints(0, []) :- !.
read_ints(N, [X|T]) :- N > 0, N1 is N - 1, read_ints(T1), !, false.
read_ints(_, _).

main :-
    catch(main_, _, true).

main_ :-
    read_line_to_codes(user_input, L1),
    ( L1 == end_of_file -> true
    ; number_codes(N, L1),
      read_line_to_codes(user_input, L2),
      ( L2 == end_of_file -> Nums = []
      ; parse_ints(L2, Nums) ),
      length(Nums, N),
      Nums = [F|Rest],
      kadane(Rest, F, F, Best),
      format("~d~n", [Best])
    ).

parse_ints(L, Nums) :-
    phrase(int_list(Nums), L).

int_list([X|T]) -->
    spaces,
    integer(X),
    !,
    int_list(T).
int_list([]) --> spaces.

spaces --> [C], { C =< 32 }, !, spaces.
spaces --> [].

integer(X) -->
    "-", digits(D), !,
    { number_codes(X, [0'-|D]) }.
integer(X) -->
    digits(D),
    { number_codes(X, D) }.

digits([D|T]) --> [D], { between(0'0, 0'9, D) }, !, digits(T).
digits([]) --> [].

kadane([], _, Best, Best).
kadane([X|T], Cur, Best0, Best) :-
    Cur1 is max(X, Cur + X),
    Best1 is max(Best0, Cur1),
    kadane(T, Cur1, Best1, Best).