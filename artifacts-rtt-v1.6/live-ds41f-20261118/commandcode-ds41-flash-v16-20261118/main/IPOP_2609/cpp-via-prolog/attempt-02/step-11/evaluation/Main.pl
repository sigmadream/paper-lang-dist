main :-
    read_all_codes(Codes),
    split_ws(Codes, Tokens),
    Tokens = [ACodes, BCodes|_],
    number_codes(A, ACodes),
    number_codes(B, BCodes),
    gcd(A, B, G),
    L is (A // G) * B,
    writeln(G),
    writeln(L).

read_all_codes(Codes) :-
    current_input(Stream),
    read_all_codes_(Stream, Codes).

read_all_codes_(Stream, Codes) :-
    get_char(Stream, C),
    ( C == end_of_file ->
        Codes = []
    ;   Codes = [C|Rest],
        read_all_codes_(Stream, Rest)
    ).

split_ws([], []).
split_ws([C|Cs], Tokens) :-
    is_space(C), !,
    split_ws(Cs, Tokens).
split_ws(Cs, [Token|Tokens]) :-
    take_token(Cs, Token, Rest),
    split_ws(Rest, Tokens).

take_token([], [], []).
take_token([C|Cs], Token, Rest) :-
    ( is_space(C) ->
        Token = [],
        Rest = [C|Cs]
    ;   Token = [C|TokenRest],
        take_token(Cs, TokenRest, Rest)
    ).

is_space(32).
is_space(9).
is_space(10).
is_space(13).

gcd(A, 0, A) :- !.
gcd(A, B, G) :-
    R is A mod B,
    gcd(B, R, G).