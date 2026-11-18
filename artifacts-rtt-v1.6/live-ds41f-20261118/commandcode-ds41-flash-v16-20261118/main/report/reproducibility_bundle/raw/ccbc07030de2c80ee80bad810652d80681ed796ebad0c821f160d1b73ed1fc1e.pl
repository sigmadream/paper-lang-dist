main :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file -> true
    ; split_string(Line, " \t\n\r", " \t\n\r", Parts),
      Parts = [MS, NS],
      number_string(M, MS),
      number_string(N, NS),
      ( M > 2 -> Start = M ; Start = 2 ),
      make_array(N, Arr),
      sieve(N, Arr),
      forall(between(Start, N, I),
             ( arg(I, Arr, true) -> writeln(I) ; true ))
    ).

make_array(N, Arr) :-
    length(Vars, N),
    maplist(=(true), Vars),
    Arr =.. [a|Vars].

sieve(N, Arr) :-
    ( N >= 1 -> setarg(1, Arr, false) ; true ),
    Sqrt is floor(sqrt(N)),
    forall(between(2, Sqrt, I),
           ( arg(I, Arr, true) ->
               J0 is I*I,
               ( J0 =< N ->
                   MaxK is (N - J0) // I + 1,
                   forall(between(1, MaxK, K),
                          ( J is J0 + (K-1)*I,
                            setarg(J, Arr, false)
                          ))
               ; true
               )
           ; true
           )
    ).