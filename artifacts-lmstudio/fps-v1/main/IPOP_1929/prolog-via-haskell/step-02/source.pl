is_prime(N) :-
    N < 2, !, fail.
is_prime(N) :-
    findall(D, (between(2, FloorSqrtN, D), N mod D =:= 0), Divisors),
    length(Divisors, 0).
is_prime(N) :-
    sqrt(N, FloorSqrtN).

main :-
    read_line(Input),
    split_string(Input, ' ', _, [MStr, HStr]),
    string_to_integer(MStr, M),
    string_to_integer(HStr, H),
    between(M, H, N),
    is_prime(N),
    write(N), nl,
    fail.
main.

read_line(Line) :-
    read_line(_, Line).

read_line(Stream, []) :-
    at_end_of_stream(Stream).
read_line(Stream, [H|T]) :-
    get_code(Stream, C),
    (   C =:= 10 -> T = [];
        true -> H is C, read_line(Stream, T)
    ).

split_string([], _, _, []).
split_string([H|T], Delimiter, CurrentWord, Result) :-
    H = Delimiter,
    !,
    split_string(T, Delimiter, [], [CurrentWord|Result]).
split_string([H|T], Delimiter, CurrentWord, Result) :-
    append(CurrentWord, [H], NewWord),
    split_string(T, Delimiter, NewWord, Result).