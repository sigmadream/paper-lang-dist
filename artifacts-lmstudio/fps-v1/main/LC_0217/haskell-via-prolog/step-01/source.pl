duplicate([H|T], H, _).
duplicate([H|T], _, Rest) :-
    member(H, T),
    duplicate(T, H, Rest).
duplicate([_|T], X, Rest) :-
    duplicate(T, X, Rest).

main :-
    read_line(Input),
    split_string(Input, ' ', '', Parts),
    maplist(atom_number, Parts, Numbers),
    length(Numbers, N),
    take(N, Numbers, SubList),
    (duplicate(SubList, _, _) -> write(1); write(0)),
    nl.

take(0, _, []).
take(N, [H|T], [H|Rest]) :-
    N > 0,
    M is N - 1,
    take(M, T, Rest).

split_string(String, Delimiter, '', Result) :-
    string_chars(String, Chars),
    split_string(Chars, Delimiter, [], Result).
split_string([], _, Current, [Current]).
split_string([H|T], Delimiter, Current, Result) :-
    H = Delimiter,
    !,
    append(Current, [''], NewCurrent),
    split_string(T, Delimiter, NewCurrent, Result).
split_string([H|T], Delimiter, Current, Result) :-
    append(Current, [H], NewCurrent),
    split_string(T, Delimiter, NewCurrent, Result).

atom_number(A, N) :-
    atom_chars(A, Chars),
    number_chars(N, Chars).