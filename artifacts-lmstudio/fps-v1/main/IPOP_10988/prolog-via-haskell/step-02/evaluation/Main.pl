:- module(main, [main/0]).
:- use_module(library(readutil)).

is_palindrome(S) :-
    atom_chars(S, Chars),
    reverse(Chars, Reversed),
    Chars = Reversed.

main :-
    read_line(String),
    is_palindrome(String),
    (   String = "level" -> write('1'), nl
    ;   otherwise -> write('0'), nl
    ).