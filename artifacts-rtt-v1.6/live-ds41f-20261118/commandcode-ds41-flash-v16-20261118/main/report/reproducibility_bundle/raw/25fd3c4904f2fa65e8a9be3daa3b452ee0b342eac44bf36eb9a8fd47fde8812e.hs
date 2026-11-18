module Main where

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (nstr:rest) ->
            let n = read nstr :: Int
                xs = map read (take n rest) :: [Integer]
            in if n <= 0 || null xs
                then return ()
                else print (kadane xs)
  where
    kadane (x:xs) = go x x xs
      where
        go cur best [] = best
        go cur best (y:ys) =
            let cur' = max y (cur + y)
                best' = max best cur'
            in go cur' best' ys
    kadane [] = 0