main :-
    read_all_codes(Codes),
    string_codes(S, Codes),
    split_string(S, " \t\n\r", " \t\n\r", Parts0),
    exclude(=(""), Parts0, Parts),
    maplist(number_string, Nums, Parts),
    Nums = [A, B | _],
    gcd(A, B, G),
    L is (A // G) * B,
    format("~w~n~w~n", [G, L]).

gcd(A, 0, A) :- !.
gcd(A, B, G) :-
    R is A mod B,
    gcd(B, R, G).

read_all_codes(Codes) :-
    read_line_to_codes(user_input, Line),
    ( Line == end_of_file -> Codes = []
    ; append(Line, [10 | Rest], Codes),
      read_all_codes(Rest)
    ).