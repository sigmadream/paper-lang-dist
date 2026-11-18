:- use_module(library(readutil)).
:- use_module(library(lists)).

main :-
    read_all_tokens(Tokens),
    Tokens = [NStr, CStr | Rest],
    number_string(N, NStr),
    number_string(C, CStr),
    take_n_tokens(N, Rest, CoordTokens),
    parse_numbers(CoordTokens, Coords),
    sort(Coords, Sorted),
    Sorted = [First | _],
    last(Sorted, Last),
    MaxDist is Last - First,
    binary_loop(Sorted, C, 1, MaxDist, 0, Answer),
    format('~w~n', [Answer]).

read_all_tokens(Tokens) :-
    read_all_acc([], RevTokens),
    reverse(RevTokens, Tokens).

read_all_acc(Acc, Tokens) :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  Tokens = Acc
    ;   split_string(Line, " \t\r", " \t\r", Raw),
        exclude(==(""), Raw, LineTokens),
        reverse(LineTokens, RevLineTokens),
        append(RevLineTokens, Acc, Acc1),
        read_all_acc(Acc1, Tokens)
    ).

take_n_tokens(0, _, []) :- !.
take_n_tokens(N, [T | Ts], [T | Taken]) :-
    N > 0,
    N1 is N - 1,
    take_n_tokens(N1, Ts, Taken).

parse_numbers([], []).
parse_numbers([Tok | Toks], [Num | Nums]) :-
    number_string(Num, Tok),
    parse_numbers(Toks, Nums).

binary_loop(Sorted, C, Left, Right, Best, Answer) :-
    (   Left > Right
    ->  Answer = Best
    ;   Mid is Left + ((Right - Left) // 2),
        (   can_place(Sorted, C, Mid)
        ->  NewLeft is Mid + 1,
            binary_loop(Sorted, C, NewLeft, Right, Mid, Answer)
        ;   NewRight is Mid - 1,
            binary_loop(Sorted, C, Left, NewRight, Best, Answer)
        )
    ).

can_place([First | Rest], C, Dist) :-
    can_rest(Rest, First, Dist, 1, C).

can_rest(_, _, _, Count, C) :- Count >= C, !.
can_rest([X | Xs], Prev, Dist, Count, C) :-
    (   X - Prev >= Dist
    ->  Count1 is Count + 1,
        can_rest(Xs, X, Dist, Count1, C)
    ;   can_rest(Xs, Prev, Dist, Count, C)
    ).