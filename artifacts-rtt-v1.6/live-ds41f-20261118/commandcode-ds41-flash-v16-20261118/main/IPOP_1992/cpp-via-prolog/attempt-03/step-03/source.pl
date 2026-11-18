:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, NLine),
    (   NLine == end_of_file
    ->  true
    ;   number_string(N, NLine),
        read_rows(N, RowStrings),
        maplist(string_chars, RowStrings, Rows),
        solve(Rows, OutChars),
        string_chars(OutStr, OutChars),
        format("~s~n", [OutStr])
    ).

read_rows(0, []) :- !.
read_rows(N, [Line|Lines]) :-
    read_line_to_string(user_input, Line),
    N1 is N - 1,
    read_rows(N1, Lines).

solve(Rows, Out) :-
    Rows = [FirstRow|_],
    FirstRow = [First|_],
    (   same_rows(Rows, First)
    ->  Out = [First]
    ;   length(Rows, N),
        H is N // 2,
        split_rows(Rows, H, Top, Bottom),
        split_cols(Top, H, TL, TR),
        split_cols(Bottom, H, BL, BR),
        solve(TL, A),
        solve(TR, B),
        solve(BL, C),
        solve(BR, D),
        append(A, B, AB),
        append(AB, C, ABC),
        append(ABC, D, ABCD),
        append(ABCD, [')'], Tail),
        Out = ['('|Tail]
    ).

same_rows([], _).
same_rows([Row|Rows], C) :-
    all_same(Row, C),
    same_rows(Rows, C).

all_same([], _).
all_same([X|Xs], C) :-
    X == C,
    all_same(Xs, C).

split_rows(Rows, 0, [], Rows) :- !.
split_rows([R|Rs], N, [R|Ls], Right) :-
    N > 0,
    N1 is N - 1,
    split_rows(Rs, N1, Ls, Right).

split_cols([], _, [], []).
split_cols([Row|Rows], H, [L|Ls], [R|Rs]) :-
    split_list(Row, H, L, R),
    split_cols(Rows, H, Ls, Rs).

split_list(List, 0, [], List) :- !.
split_list([X|Xs], N, [X|Ls], R) :-
    N > 0,
    N1 is N - 1,
    split_list(Xs, N1, Ls, R).