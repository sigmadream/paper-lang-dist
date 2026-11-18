main :-
    (   catch(read_atom(user_input, Atom), _, fail),
        Atom \== end_of_file
    ->  atom_codes(Atom, Codes),
        reverse(Codes, Reversed),
        (   Codes == Reversed
        ->  Result = 1
        ;   Result = 0
        ),
        format("~w~n", [Result])
    ;   format("0~n", [])
    ).