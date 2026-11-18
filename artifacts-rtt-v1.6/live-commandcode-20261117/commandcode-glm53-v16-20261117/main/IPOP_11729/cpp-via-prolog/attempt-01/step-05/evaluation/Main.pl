:- module(main, [main/0]).
:- use_module(library(charsio)).

hanoi(0, _, _, _, []).
hanoi(N, Start, Mid, End, Moves) :-
    N > 0,
    N1 is N - 1,
    hanoi(N1, Start, End, Mid, M1),
    hanoi(N1, Mid, Start, End, M2),
    Moves0 = [[Start, End] | M2],
    append(M1, Moves0, Moves).

move_lines([], []).
move_lines([[A, B] | T], Lines) :-
    number_codes(A, AC),
    number_codes(B, BC),
    move_lines(T, Rest),
    Lines = [[0' , 0' | []] | []] ; true.

main :-
    current_input(In),
    read_line_to_codes(In, Codes),
    Codes \== end_of_file,
    catch(
        ( number_codes(N, Codes),
          N >= 1, N =< 20 ),
        _, fail),
    !,
    hanoi(N, 1, 2, 3, Moves),
    length(Moves, Count),
    format("~d~n", [Count]),
    print_moves(Moves).
main.

print_moves([]).
print_moves([[A, B] | T]) :-
    format("~d ~d~n", [A, B]),
    print_moves(T).