:- use_module(library(readutil)).

palindrome(S) :-
    reverse(S, S).

main :-
    read_line_to_string(CurrentLine),
    atom_chars(CurrentLine, Chars),
    palindrome(Chars),
    write('1'), nl.
main :-
    read_line_to_string(CurrentLine),
    atom_chars(CurrentLine, Chars),
    \+ palindrome(Chars),
    write('0'), nl.