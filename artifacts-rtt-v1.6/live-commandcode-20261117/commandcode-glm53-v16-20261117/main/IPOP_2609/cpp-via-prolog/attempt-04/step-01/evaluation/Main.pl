:- module(main, []).
:- use_module(library(readutil)).

main :-
    catch((current_input(In),
           read_line_to_codes(In, Line),
           Line \= end_of_file,
           split_line(Line, [A, B]),
           G is gcd(A, B),
           L is (A // G) * B,
           format("~d~n~d~n", [G, L])), true).

split_line(Line, Nums) :-
    split(Line, [32], Tokens),
    maplist(number_codes, Nums, Tokens).