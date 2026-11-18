main :-
    (   read_line_to_string(user_input, TStr),
        TStr \== end_of_file,
        number_string(T, TStr)
    ->  process(T)
    ;   true
    ).

process(0) :- !.
process(N) :-
    read_line_to_string(user_input, S),
    (   S == end_of_file
    ->  write('NO')
    ;   (   valid(S)
        ->  write('YES')
        ;   write('NO')
        )
    ),
    nl,
    N1 is N - 1,
    process(N1).

valid(S) :-
    string_chars(S, Chars),
    valid_loop(Chars, 0).

valid_loop([], 0).
valid_loop(['('|Rest], Balance) :-
    Balance1 is Balance + 1,
    valid_loop(Rest, Balance1).
valid_loop([')'|Rest], Balance) :-
    Balance > 0,
    Balance1 is Balance - 1,
    valid_loop(Rest, Balance1).