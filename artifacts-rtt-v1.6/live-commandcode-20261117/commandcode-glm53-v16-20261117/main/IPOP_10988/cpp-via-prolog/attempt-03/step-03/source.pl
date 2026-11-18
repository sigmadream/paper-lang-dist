:- module(main, [main/0]).
:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, S),
    ( S == end_of_file ->
        true
    ; string_codes(S, Codes),
      reverse(Codes, Rev),
      ( Codes == Rev -> R = 1 ; R = 0 ),
      format("~d~n", [R])
    ).