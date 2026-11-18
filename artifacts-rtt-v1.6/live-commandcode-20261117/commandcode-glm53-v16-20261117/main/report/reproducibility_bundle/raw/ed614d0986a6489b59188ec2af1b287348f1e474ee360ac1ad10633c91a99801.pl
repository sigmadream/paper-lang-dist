:- module(main, [main/0]).
:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, L1),
    ( L1 == end_of_file -> true
    ; number_codes(N, L1),
      read_line_to_codes(user_input, L2),
      ( L2 == end_of_file -> Nums = []
      ; split_and_numbers(L2, Nums)
      ),
      length(Nums, N),
      Nums = [H|T],
      kadane(T, H, H, Best),
      write(Best), nl
    ).

split_and_numbers(Codes, Nums) :-
    phrase(numbers(Nums), Codes).

numbers([X|Xs]) -->
    blanks,
    integer(X),
    !,
    numbers(Xs).
numbers([]) -->
    [].

blanks -->
    [C], { code_type(C, space), ! },
    blanks.
blanks -->
    [].

integer(X) -->
    sign(S),
    digits(D),
    { number_codes(X0, D), X is S * X0 }.

sign(-1) --> "-", !.
sign(1) --> [].

digits([C|Cs]) -->
    [C], { code_type(C, digit) },
    digits(Cs).
digits([C]) -->
    [C], { code_type(C, digit) }.

kadane([], _, Best, Best).
kadane([X|Xs], Cur0, Best0, Best) :-
    Cur1 is max(X, Cur0 + X),
    Best1 is max(Best0, Cur1),
    kadane(Xs, Cur1, Best1, Best).