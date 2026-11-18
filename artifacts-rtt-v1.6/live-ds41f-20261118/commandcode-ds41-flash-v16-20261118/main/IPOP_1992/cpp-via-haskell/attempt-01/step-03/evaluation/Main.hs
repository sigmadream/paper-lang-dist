module Main where

main :: IO ()
main = do
    input <- getContents
    case lines input of
        [] -> return ()
        (nStr : rest) ->
            let n = read nStr :: Int
                grid = take n rest
            in putStrLn (solve grid 0 0 n)

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size
    | sameRegion = [first]
    | otherwise = "("
        ++ solve grid r c half
        ++ solve grid r (c + half) half
        ++ solve grid (r + half) c half
        ++ solve grid (r + half) (c + half) half
        ++ ")"
  where
    first = grid !! r !! c
    sameRegion = all (== first)
        [ grid !! i !! j
        | i <- [r .. r + size - 1]
        , j <- [c .. c + size - 1]
        ]
    half = size `div` 2