:- module(main, [main/0]).
:- use_module(library(readutil)).

main :-
    catch(run, _, true).

run :-
    read_line_to_codes(user_input, L1),
    ( L1 == end_of_file -> true
    ; number_codes(N, L1),
      N > 0,
      read_line_to_codes(user_input, L2),
      atom_codes(A2, L2),
      split_string(A2, " ", " ", Parts),
      maplist(number_string, A, Parts),
      A = [H|T],
      foldl(step, T, H-H, _-Best),
      format("~d~n", [Best])
    ).

step(X, Cur0-Best0, Cur-Best) :-
    Cur1 is max(X, Cur0 + X),
    Best is max(Best0, Cur1),
    Cur = Cur1.