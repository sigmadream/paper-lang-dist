:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, codes).

read_int(I) :- read_line_codes(Cs), parse_int(Cs, I), !.
read_int(_) :- halt.

read_line_codes(Cs) :-
    get_code(C),
    ( C == -1 -> Cs = []
    ; C == 10 -> Cs = []
    ; C == 13 -> read_line_codes(Cs)
    ; Cs = [C|Rest], read_line_codes(Rest)
    ).

parse_int(Cs, I) :-
    number_codes(I, Cs).

split_ints([], []).
split_ints(Cs, [I|Is]) :-
    skip_ws(Cs, Cs1),
    ( Cs1 == [] -> Is = []
    ; take_int(Cs1, Digits, Rest),
      number_codes(I, Digits),
      split_ints(Rest, Is)
    ).

skip_ws([C|Cs], Rest) :- ( C == 32 ; C == 9 ), !, skip_ws(Cs, Rest).
skip_ws(Cs, Cs).

take_int([C|Cs], [C|Ds], Rest) :- C \== 32, !, take_int(Cs, Ds, Rest).
take_int(Cs, [], Cs).

read_all_ints(Is) :-
    read_line_codes(L1),
    ( L1 == [] -> Is = []
    ; parse_int(_, L1) -> true
    ; true
    ),
    fail. % placeholder never used

main :-
    read_line_codes(Line1),
    parse_int(Line1, N),
    read_line_codes(Line2),
    split_ints(Line2, Values),
    length(Values, N),
    partition_zeroes(Values, NonZeros, Zeros),
    append(NonZeros, Zeros, Result),
    print_list(Result).

partition_zeroes([], [], []).
partition_zeroes([X|Xs], [X|Ns], Zs) :- X =\= 0, !, partition_zeroes(Xs, Ns, Zs).
partition_zeroes([X|Xs], Ns, [X|Zs]) :- partition_zeroes(Xs, Ns, Zs).

print_list([]) :- nl.
print_list([X]) :- !, write(X), nl.
print_list([X|Xs]) :- write(X), write(' '), print_list(Xs).