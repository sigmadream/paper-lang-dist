:- module(main, [main/0]).
:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, Codes),
    (   Codes == end_of_file
    ->  true
    ;   string_codes(Str, Codes),
        split_string(Str, " ", " \t\r\n", Parts),
        Parts = [A, B],
        number_string(M, A),
        number_string(N, B),
        Total is M + N - 2,
        K is M - 1,
        K0 is min(K, Total - K),
        comb(Total, K0, Result),
        writeln(Result)
    ).

comb(_, 0, 1) :- !.
comb(N, K, R) :-
    K1 is K - 1,
    comb(N, K1, R1),
    R is R1 * (N - K + 1) // K.