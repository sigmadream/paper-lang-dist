:- module(main, [main/0]).

hanoi(1, Start, _, End, [[Start, End]]) :- !.
hanoi(N, Start, Mid, End, Moves) :-
    N1 is N - 1,
    hanoi(N1, Start, End, Mid, M1),
    hanoi(N1, Mid, Start, End, M2),
    append(M1, [[Start, End]|M2], Moves).

print_moves([]).
print_moves([[A, B]|T]) :-
    format("~d ~d~n", [A, B]),
    print_moves(T).

main :-
    current_input(In),
    read_line_to_codes(In, Codes),
    ( Codes == end_of_file -> true
    ; catch(number_codes(N, Codes), _, fail) ->
      ( N < 1 -> true
      ; hanoi(N, 1, 2, 3, Moves),
        length(Moves, Count),
        format("~d~n", [Count]),
        print_moves(Moves)
      )
    ; true
    ).