:- use_module(library(readutil)).

main :-
    read_n(N),
    build_counts(N, Counts),
    atomic_list_concat(Counts, ' ', Out),
    format("~w~n", [Out]).

read_n(N) :-
    read_line_to_codes(user_input, Codes),
    (   Codes == end_of_file
    ->  N = 0
    ;   filter_int_codes(Codes, Filtered),
        (   Filtered == []
        ->  N = 0
        ;   number_codes(N, Filtered)
        )
    ).

filter_int_codes([], []).
filter_int_codes([C|Cs], Out) :-
    (   C =:= 0'- 
    ;   C >= 0'0, C =< 0'9
    )
    ->  Out = [C|Rest],
        filter_int_codes(Cs, Rest)
    ;   filter_int_codes(Cs, Out).

build_counts(N, Counts) :-
    build_counts_acc(0, N, [], Rev),
    reverse_list(Rev, [], Counts).

build_counts_acc(I, N, Acc, Rev) :-
    I =< N,
    bit_count(I, C),
    I1 is I + 1,
    build_counts_acc(I1, N, [C|Acc], Rev).
build_counts_acc(I, N, Acc, Acc) :-
    I > N.

bit_count(0, 0) :- !.
bit_count(N, C) :-
    N > 0,
    Q is N // 2,
    R is N mod 2,
    bit_count(Q, Cq),
    C is Cq + R.

reverse_list([], Acc, Acc).
reverse_list([X|Xs], Acc, Result) :-
    reverse_list(Xs, [X|Acc], Result).