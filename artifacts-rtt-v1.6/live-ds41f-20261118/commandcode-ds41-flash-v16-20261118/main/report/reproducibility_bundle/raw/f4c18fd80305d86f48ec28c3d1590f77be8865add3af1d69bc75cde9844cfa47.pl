main :-
    read_all_codes(Codes),
    tokenize(Codes, Tokens),
    Tokens = [NToken|RowTokens],
    number_codes(N, NToken),
    take(N, RowTokens, Rows),
    solve(Rows, N, Out),
    format("~s~n", [Out]).

read_all_codes(Codes) :-
    get_char(C),
    read_all_codes_(C, Codes).

read_all_codes_(end_of_file, []) :- !.
read_all_codes_(C, [Code|Codes]) :-
    char_code(C, Code),
    get_char(D),
    read_all_codes_(D, Codes).

tokenize([], []).
tokenize([C|Cs], Tokens) :-
    is_space(C), !,
    tokenize(Cs, Tokens).
tokenize([C|Cs], [Token|Tokens]) :-
    take_token(Cs, [C], Token, Rest),
    tokenize(Rest, Tokens).

is_space(32).
is_space(10).
is_space(9).
is_space(13).

take_token([], Acc, Token, []) :-
    reverse(Acc, Token).
take_token([C|Cs], Acc, Token, Rest) :-
    is_space(C), !,
    reverse(Acc, Token),
    Rest = Cs.
take_token([C|Cs], Acc, Token, Rest) :-
    \+ is_space(C),
    take_token(Cs, [C|Acc], Token, Rest).

take(0, _, []) :- !.
take(N, [X|Xs], [X|Ys]) :-
    N > 0,
    N1 is N - 1,
    take(N1, Xs, Ys).

solve(Rows, Size, Out) :-
    Rows = [FirstRow|_],
    FirstRow = [First|_],
    ( all_same(Rows, First) ->
        Out = [First]
    ; Half is Size // 2,
      split_region(Rows, Half, TL, TR, BL, BR),
      solve(TL, Half, S1),
      solve(TR, Half, S2),
      solve(BL, Half, S3),
      solve(BR, Half, S4),
      append([[40|S1], S2, S3, S4, [41]], Out)
    ).

all_same([Row|Rows], First) :-
    all_elems_same(Row, First),
    all_rows_same(Rows, First).

all_rows_same([], _).
all_rows_same([Row|Rows], First) :-
    all_elems_same(Row, First),
    all_rows_same(Rows, First).

all_elems_same([], _).
all_elems_same([X|Xs], First) :-
    X =:= First,
    all_elems_same(Xs, First).

split_region(Rows, Half, TL, TR, BL, BR) :-
    split_n(Rows, Half, TopRows, BottomRows),
    split_each(TopRows, Half, TL, TR),
    split_each(BottomRows, Half, BL, BR).

split_n(Rows, 0, [], Rows) :- !.
split_n([Row|Rows], K, [Row|A], B) :-
    K > 0,
    K1 is K - 1,
    split_n(Rows, K1, A, B).

split_each([], _, [], []).
split_each([Row|Rows], K, [L|Ls], [R|Rs]) :-
    split_n(Row, K, L, R),
    split_each(Rows, K, Ls, Rs).