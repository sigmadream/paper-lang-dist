:- module(main, [main/0]).
:- use_module(library(dcgs)).

main :-
    read_line_to_codes(user_input, L1),
    ( L1 == end_of_file -> true
    ; L1 \== end_of_file ->
        phrase(number(N), L1, _),
        read_line_to_codes(user_input, L2),
        ( L2 == end_of_file -> Rest = []
        ; phrase(numbers(Rest), L2, _),
          read_remaining(Rest2),
          append(Rest, Rest2, Nums)
        ),
        ( Nums == [] -> true
        ; kadane(Nums, Best),
          number_codes(Best, Codes),
          append(Codes, "\n", Out),
          format("~s", [Out])
        )
    ).

read_remaining(Acc) :-
    read_line_to_codes(user_input, L),
    ( L == end_of_file -> Acc = []
    ; phrase(numbers(Ns), L, _),
      read_remaining(More),
      append(Ns, More, Acc)
    ).

numbers([]) --> [].
numbers([N|T]) -->
    ( " " -> [] ; "\t" -> [] ; "\n" -> [] ),
    number(N),
    numbers(T).

number(N) -->
    ( "-" -> [C], { C >= 48, C =< 57, N is C - 48 }, digits(A), { N1 is -(A) }, number_rest(N1, N)
    ; [C], { C >= 48, C =< 57 }, digits(A), number_rest(A, N)
    ).

number_rest(N, N) --> [].
number_rest(N, M) --> " ", number(M).
number_rest(N, M) --> "\t", number(M).
number_rest(N, M) --> "\n", number(M).

digits(N) --> [C], { C >= 48, C =< 57, !, D is C - 48 }, digits(T), { N is T*10 + D }.
digits(0) --> [].

kadane([X|Xs], Best) :- kadane(Xs, X, X, Best).
kadane([], _, Best, Best).
kadane([X|Xs], Cur, Best0, Best) :-
    Cur1 is max(X, Cur + X),
    Best1 is max(Best0, Cur1),
    kadane(Xs, Cur1, Best1, Best).