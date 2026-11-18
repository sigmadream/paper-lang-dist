:- use_module(library(readutil)).

main :-
    all_codes(Codes),
    tokens(Codes, Nums),
    ( Nums = [_, M | Rest] ->
        extract_edges(M, Rest, Edges),
        count_friends(Edges, Answer)
    ; Answer = 0
    ),
    write(Answer), nl.

all_codes(Codes) :-
    read_all_lines([], LinesRev),
    reverse(LinesRev, Lines),
    join_lines(Lines, Codes).

read_all_lines(Acc, Lines) :-
    read_line_to_codes(user_input, Codes),
    ( Codes == end_of_file ->
        Lines = Acc
    ; read_all_lines([Codes|Acc], Lines)
    ).

join_lines([], []).
join_lines([Line], Line) :- !.
join_lines([Line|Lines], Codes) :-
    append(Line, [32], Line1),
    join_lines(Lines, Rest),
    append(Line1, Rest, Codes).

tokens([], []).
tokens(Codes, Nums) :-
    skip_ws(Codes, Rest),
    ( Rest == [] ->
        Nums = []
    ; parse_number(Rest, Num, Rest2),
      Nums = [Num|NumsRest],
      tokens(Rest2, NumsRest)
    ).

skip_ws([C|Cs], Rest) :-
    ( C =:= 32 ; C =:= 9 ; C =:= 10 ; C =:= 13 ),
    !,
    skip_ws(Cs, Rest).
skip_ws(Cs, Cs).

parse_number([C|Cs], Num, Rest) :-
    C >= 48, C =< 57,
    Acc is C - 48,
    parse_digits(Cs, Acc, Num, Rest).

parse_digits([C|Cs], Acc, Num, Rest) :-
    C >= 48, C =< 57,
    !,
    Acc1 is Acc * 10 + C - 48,
    parse_digits(Cs, Acc1, Num, Rest).
parse_digits(Rest, Acc, Acc, Rest).

extract_edges(0, _, []) :- !.
extract_edges(K, [A,B|Rest], [A-B|Edges]) :-
    K > 0,
    K1 is K - 1,
    extract_edges(K1, Rest, Edges).

count_friends(Edges, Answer) :-
    direct_neighbors(Edges, Direct0),
    sort(Direct0, Direct),
    collect_candidates(Direct, Edges, Cand0),
    sort(Cand0, Cand),
    exclude_one(Cand, Filtered),
    length(Filtered, Answer).

direct_neighbors(Edges, Direct) :-
    findall(V,
            ( member(A-B, Edges),
              ( (A =:= 1, V = B) ; (B =:= 1, V = A) )
            ),
            Direct).

neighbors_of(V, Edges, Ns) :-
    findall(U,
            ( member(A-B, Edges),
              ( (A =:= V, U = B) ; (B =:= V, U = A) )
            ),
            Ns).

collect_candidates([], _, []).
collect_candidates([V|Vs], Edges, Cand) :-
    neighbors_of(V, Edges, Ns),
    collect_candidates(Vs, Edges, CandRest),
    append([V|Ns], CandRest, Cand).

exclude_one([], []).
exclude_one([1|T], R) :- !,
    exclude_one(T, R).
exclude_one([X|T], [X|R]) :-
    X =\= 1,
    exclude_one(T, R).