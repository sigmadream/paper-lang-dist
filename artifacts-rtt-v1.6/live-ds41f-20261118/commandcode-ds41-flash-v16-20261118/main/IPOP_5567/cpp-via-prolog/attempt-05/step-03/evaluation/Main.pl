read_ints(List) :-
    get_code(C),
    read_ints_codes(C, List).

read_ints_codes(-1, []) :- !.
read_ints_codes(C, List) :-
    skip_nondigit(C, C1),
    (   C1 =:= -1 ->
        List = []
    ;   List = [Num|Rest],
        read_number(C1, Num, Next),
        read_ints_codes(Next, Rest)
    ).

skip_nondigit(C, C1) :-
    (   C >= 48, C =< 57 ->
        C1 = C
    ;   C =:= -1 ->
        C1 = -1
    ;   get_code(C2),
        skip_nondigit(C2, C1)
    ).

read_number(C, Num, Next) :-
    read_digits(C, [], DigitsRev, Next),
    reverse(DigitsRev, Digits),
    number_codes(Num, Digits).

read_digits(C, Acc, Result, Next) :-
    (   C >= 48, C =< 57 ->
        get_code(C2),
        read_digits(C2, [C|Acc], Result, Next)
    ;   Result = Acc,
        Next = C
    ).

read_edges(0, _, []) :- !.
read_edges(M, [A,B|Rest], [A-B|Edges]) :-
    M > 0,
    M1 is M - 1,
    read_edges(M1, Rest, Edges).

adjacent(Edges, X, Y) :-
    member(A-B, Edges),
    (   X = A, Y = B
    ;   X = B, Y = A
    ).

direct_neighbors(Edges, L) :-
    findall(Y, adjacent(Edges, 1, Y), L0),
    sort(L0, L).

second_neighbors(Edges, Direct, L) :-
    findall(Y, (member(X, Direct), adjacent(Edges, X, Y), Y \= 1), L0),
    sort(L0, L).

main :-
    read_ints(Nums),
    (   Nums = [_N, M | Rest] ->
        read_edges(M, Rest, Edges),
        direct_neighbors(Edges, Direct),
        second_neighbors(Edges, Direct, Second),
        append(Direct, Second, Combined),
        sort(Combined, Unique),
        length(Unique, Ans),
        writeln(Ans)
    ;   true
    ).