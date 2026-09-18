:- use_module(library(readutil)).

main :-
    read_line_to_string(STDIN),
    string_to_list(STDIN, Input),
    parse_input(Input, N, NumList),
    move_zeroes(N, NumList, Result),
    format('~w~n', [Result]).

parse_input(Input, N, NumList) :-
    split_string(Input, ' ', '', Parts),
    maplist(string_to_integer, Parts, [N | NumList]).

move_zeroes(_, [], []).
move_zeroes(N, [0 | Rest], Result) :-
    move_zeroes(N, Rest, Tail),
    append(Tail, [0], Result).
move_zeroes(N, [H | Rest], [H | Tail]) :-
    move_zeroes(N, Rest, Tail).