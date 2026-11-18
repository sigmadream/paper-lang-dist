read_numbers(Nums) :-
    read_all_codes(Codes),
    parse_nums(Codes, Nums).

read_all_codes(Codes) :-
    read_all_codes_dl(Codes, []).

read_all_codes_dl([Code|Rest], Tail) :-
    get_char(C),
    C \== end_of_file,
    !,
    char_code(C, Code),
    read_all_codes_dl(Rest, Tail).
read_all_codes_dl(Tail, Tail).

parse_nums([], []).
parse_nums([C|Cs], Nums) :-
    ( C =< 32 ->
        parse_nums(Cs, Nums)
    ;   Num0 is C - 48,
        parse_digits(Cs, Num0, Num, Rest),
        Nums = [Num|RestNums],
        parse_nums(Rest, RestNums)
    ).

parse_digits([C|Cs], Acc, Num, Rest) :-
    C >= 48,
    C =< 57,
    !,
    Acc1 is Acc * 10 + (C - 48),
    parse_digits(Cs, Acc1, Num, Rest).
parse_digits(Rest, Acc, Acc, Rest).

take_edges(0, _, []) :- !.
take_edges(M, [A,B|Rest], [e(A,B)|Edges]) :-
    M > 0,
    M1 is M - 1,
    take_edges(M1, Rest, Edges).

neighbor(Node, [e(A,B)|_], B) :-
    A =:= Node.
neighbor(Node, [e(A,B)|_], A) :-
    B =:= Node.
neighbor(Node, [_|Es], X) :-
    neighbor(Node, Es, X).

member_l(X, [X|_]).
member_l(X, [_|T]) :-
    member_l(X, T).

append_l([], L, L).
append_l([H|T], L, [H|R]) :-
    append_l(T, L, R).

remove_one([], []).
remove_one([1|T], R) :-
    !,
    remove_one(T, R).
remove_one([H|T], [H|R]) :-
    H \= 1,
    remove_one(T, R).

solve(Edges, Ans) :-
    findall(X, neighbor(1, Edges, X), Raw1),
    sort(Raw1, L1),
    findall(Y, (member_l(X, L1), neighbor(X, Edges, Y)), Raw2),
    append_l(L1, Raw2, RawAll),
    sort(RawAll, All),
    remove_one(All, Counted),
    length(Counted, Ans).

main :-
    read_numbers(Nums),
    ( Nums = [_N, M | EdgeNums] ->
        take_edges(M, EdgeNums, Edges),
        solve(Edges, Ans),
        write(Ans),
        nl
    ;   true
    ).