:- module(main, [main/0]).

main :-
    current_input(In),
    read_line_to_codes(In, Line1),
    number_codes(N, Line1),
    read_line_to_codes(In, Line2),
    split_numbers(Line2, Nums),
    length(Nums, N),
    (   N > 0
    ->  Nums = [First|Rest],
        kadane(Rest, First, First, Best),
        format("~d~n", [Best])
    ;   true
    ).

split_numbers(Codes, Nums) :-
    phrase(numbers(Nums), Codes).

numbers([X|Xs]) -->
    ws,
    number(X),
    !,
    numbers(Xs).
numbers([]) --> ws.

ws --> [C], { code_type(C, space), ! }, ws.
ws --> [].

number(X) -->
    [C], { code_type(C, digit) ; C == 0'- },
    digits(C, Ds),
    { number_codes(X, Ds) }.

digits(C, [C|Ds]) -->
    (   [D], { code_type(D, digit), ! }
    ->  digits(D, Ds)
    ;   { Ds = [] }
    ).

kadane([], _, Best, Best).
kadane([X|Xs], Cur0, Best0, Best) :-
    Cur1 is max(X, Cur0 + X),
    Best1 is max(Best0, Cur1),
    kadane(Xs, Cur1, Best1, Best).