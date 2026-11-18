main :-
    read_all_codes(Codes),
    parse_and_run(Codes).

read_all_codes(Codes) :-
    current_input(Stream),
    read_codes(Stream, Codes).

read_codes(Stream, Codes) :-
    get_code(Stream, C),
    ( C =:= -1 ->
        Codes = []
    ;
        Codes = [C|Rest],
        read_codes(Stream, Rest)
    ).

parse_and_run(Codes) :-
    skip_ws(Codes, C1),
    take_token(C1, Token, AfterToken),
    number_codes(T, Token),
    discard_first_line(AfterToken, Rest),
    process_lines(T, Rest).

skip_ws([C|Rest], Out) :-
    is_ws_code(C),
    !,
    skip_ws(Rest, Out).
skip_ws(List, List).

take_token(Codes, Token, Rest) :-
    take_token_(Codes, Token, Rest).

take_token_([C|Cs], [C|Token], Rest) :-
    \+ is_ws_code(C),
    !,
    take_token_(Cs, Token, Rest).
take_token_(Rest, [], Rest).

discard_first_line([], []).
discard_first_line([10|Rest], Rest) :-
    !.
discard_first_line([_|Rest], Out) :-
    discard_first_line(Rest, Out).

process_lines(0, _) :-
    !.
process_lines(N, Codes) :-
    N > 0,
    ( take_line(Codes, Line, Rest) ->
        trim_codes(Line, Trimmed),
        ( valid_parens(Trimmed) ->
            write('YES'), nl
        ;
            write('NO'), nl
        ),
        N1 is N - 1,
        process_lines(N1, Rest)
    ;
        true
    ).

take_line([10|Rest], [], Rest) :-
    !.
take_line([C|Cs], Line, Rest) :-
    C =\= 10,
    take_line_chars(Cs, [C], Line, Rest).

take_line_chars([], Acc, Line, []) :-
    reverse(Acc, Line).
take_line_chars([10|Rest], Acc, Line, Rest) :-
    !,
    reverse(Acc, Line).
take_line_chars([C|Cs], Acc, Line, Rest) :-
    C =\= 10,
    take_line_chars(Cs, [C|Acc], Line, Rest).

trim_codes(Codes, Trimmed) :-
    drop_ws_front(Codes, C1),
    reverse(C1, Rev),
    drop_ws_front(Rev, Rev2),
    reverse(Rev2, Trimmed).

drop_ws_front([C|Rest], Out) :-
    is_ws_code(C),
    !,
    drop_ws_front(Rest, Out).
drop_ws_front(List, List).

valid_parens(Codes) :-
    Codes \= [],
    valid_parens_loop(Codes, 0).

valid_parens_loop([], Balance) :-
    Balance =:= 0.
valid_parens_loop([40|Rest], Balance) :-
    B1 is Balance + 1,
    valid_parens_loop(Rest, B1).
valid_parens_loop([41|Rest], Balance) :-
    Balance > 0,
    B1 is Balance - 1,
    valid_parens_loop(Rest, B1).
valid_parens_loop([_|_], _) :-
    fail.

is_ws_code(9).
is_ws_code(10).
is_ws_code(11).
is_ws_code(12).
is_ws_code(13).
is_ws_code(32).