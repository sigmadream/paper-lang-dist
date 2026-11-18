:- module(main, [main/0]).
:- use_module(library(dcg/basics)).

main :-
    read_line_to_codes(user_input, Codes),
    ( Codes == end_of_file -> true
    ; reverse(Codes, Reversed),
      ( Codes == Reversed -> write(1), nl ; write(0), nl )
    ).