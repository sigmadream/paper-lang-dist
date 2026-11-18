main :-
    read_line_to_codes(user_input, Codes),
    ( Codes == end_of_file ->
        true
    ;
        tokenize_codes(Codes, Tokens),
        Tokens = [MCodes, NCodes|_],
        number_codes(M, MCodes),
        number_codes(N, NCodes),
        unique_paths(M, N, Answer),
        writeln(Answer)
    ).

tokenize_codes([], []).
tokenize_codes([C|Cs], Tokens) :-
    code_type(C, space), !,
    tokenize_codes(Cs, Tokens).
tokenize_codes(Cs, [Token|Tokens]) :-
    take_nonspace(Cs, Token, Rest),
    tokenize_codes(Rest, Tokens).

take_nonspace([], [], []).
take_nonspace([C|Cs], [], Rest) :-
    code_type(C, space), !,
    Rest = Cs.
take_nonspace([C|Cs], [C|Token], Rest) :-
    take_nonspace(Cs, Token, Rest).

unique_paths(M, N, Answer) :-
    make_ones(N, Row0),
    Rows is M - 1,
    iterate_rows(Rows, Row0, Row),
    last_element(Row, Answer).

make_ones(0, []) :- !.
make_ones(N, [1|Rest]) :-
    N > 0,
    N1 is N - 1,
    make_ones(N1, Rest).

iterate_rows(0, Row, Row) :- !.
iterate_rows(K, Row, Result) :-
    update_row(Row, Updated),
    K1 is K - 1,
    iterate_rows(K1, Updated, Result).

update_row([First|Rest], [First|NewRest]) :-
    update_rest(Rest, First, NewRest).

update_rest([], _, []).
update_rest([X|Xs], Prev, [Y|Ys]) :-
    Y is Prev + X,
    update_rest(Xs, Y, Ys).

last_element([X], X) :- !.
last_element([_|Tail], X) :-
    last_element(Tail, X).