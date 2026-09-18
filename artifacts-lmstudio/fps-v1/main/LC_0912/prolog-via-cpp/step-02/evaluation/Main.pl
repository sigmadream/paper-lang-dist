merge([], [], []).
merge([H1|T1], [], [H1|T]) :- merge(T1, [], T).
merge([], [H2|T2], [H2|T]) :- merge([], T2, T).
merge([H1|T1], [H2|T2], [H1|T]) :-
    H1 =< H2,
    merge(T1, [H2|T2], T).
merge([H1|T1], [H2|T2], [H2|T]) :-
    H1 > H2,
    merge([H1|T1], T2, T).

mergeSort([], []).
mergeSort([X], [X]).
mergeSort(List, Sorted) :-
    split(List, Left, Right),
    mergeSort(Left, SortedLeft),
    mergeSort(Right, SortedRight),
    merge(SortedLeft, SortedRight, Sorted).

split([], [], []).
split([H|T], [H|Left], Right) :- split(T, Right, Left).

main :-
    read_line_to_string(_, Input),
    string_to_list(Input, Chars),
    maplist(char_code, Chars, Codes),
    append([N|Numbers], _, Codes),
    number_codes(N, NInt),
    length(Numbers, Length),
    number_codes(Length, LengthInt),
    sub_string(Numbers, 0, LengthInt, _, NumberCodes),
    maplist(number_codes, NumberCodes, NumbersInts),
    mergeSort(NumbersInts, SortedNumbers),
    maplist(number_codes, SortedNumbers, SortedNumberCodes),
    string_concat(SortedNumberCodes, Output),
    write(Output), nl.