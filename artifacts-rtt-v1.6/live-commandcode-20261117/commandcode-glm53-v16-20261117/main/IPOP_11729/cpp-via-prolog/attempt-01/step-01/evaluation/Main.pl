:- module(main, [main/0]).
:- use_module(library(charsio)).

read_int(N) :-
    read_line_to_string(S),
    ( S == end_of_file -> N = 0
    ; string_codes(S, Cs), number_codes(N, Cs) ).

read_line_to_string(S) :-
    read_line(Codes),
    ( Codes == end_of_file -> S = end_of_file
    ; atom_codes(S, Codes) ).

read_line(Codes) :-
    current_input(In),
    read_line_to_codes(In, Codes).

read_line_to_codes(Stream, Codes) :-
    get_code(Stream, C0),
    read_line_rest(Stream, C0, Codes).

read_line_rest(_, end_of_file, end_of_file) :- !.
read_line_rest(Stream, C, []) :-
    ( C == 10 ; C == 13 ; C == -1 ), !,
    ( C == 13 -> get_code(Stream, C2),
                 ( C2 == 10 -> true ; putback_code(Stream, C2) )
    ; true ).
read_line_rest(Stream, C, [C|Rest]) :-
    get_code(Stream, C2),
    read_line_rest(Stream, C2, Rest).

putback_code(Stream, C) :-
    peek_code(Stream, C).

hanoi(1, Start, _, End, [[Start, End]]) :- !.
hanoi(N, Start, Mid, End, Moves) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, Start, End, Mid, M1),
    hanoi(N1, Mid, Start, End, M2),
    append(M1, [[Start, End]|M2], Moves).

main :-
    read_int(N),
    ( N >= 1 ->
        hanoi(N, 1, 2, 3, Moves),
        length(Moves, Count),
        format("~d~n", [Count]),
        print_moves(Moves)
    ; true ).

print_moves([]).
print_moves([[A, B]|Rest]) :-
    format("~d ~d~n", [A, B]),
    print_moves(Rest).