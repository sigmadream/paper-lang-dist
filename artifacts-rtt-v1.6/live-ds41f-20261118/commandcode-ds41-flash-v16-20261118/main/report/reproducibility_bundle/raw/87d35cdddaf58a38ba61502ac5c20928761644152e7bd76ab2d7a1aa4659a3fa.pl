main :-
    catch(read_string(user_input, end_of_file, Str), _, Str = ""),
    ( Str == "" -> true
    ; split_string(Str, " \t\n\r", " \t\n\r", Parts),
      ( Parts = [AStr, BStr | _] ->
          number_string(A, AStr),
          number_string(B, BStr),
          gcd(A, B, G),
          L is (A // G) * B,
          format("~w~n~w~n", [G, L])
      ; true
      )
    ).

gcd(A, B, G) :-
    ( B =:= 0 -> G = A
    ; R is A mod B,
      gcd(B, R, G)
    ).