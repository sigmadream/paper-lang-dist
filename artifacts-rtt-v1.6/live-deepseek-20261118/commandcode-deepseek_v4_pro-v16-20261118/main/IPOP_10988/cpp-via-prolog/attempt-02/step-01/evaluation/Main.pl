:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Input),
    (   Input = end_of_file
    ->  true
    ;   (   palindrome(Input)
        ->  writeln('1')
        ;   writeln('0')
        )
    ).

palindrome(S) :-
    reverse(S, S).