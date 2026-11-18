module Main where

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size
    | same = [first]
    | otherwise = "(" ++
        solve grid r c half ++
        solve grid r (c + half) half ++
        solve grid (r + half) c half ++
        solve grid (r + half) (c + half) half ++
        ")"
  where
    first = grid !! r !! c
    half = size `div` 2
    same = all (\i -> all (\j -> grid !! i !! j == first)
                         [c .. c + size - 1])
               [r .. r + size - 1]

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        [] -> return ()
        (nStr : rest) -> do
            let n = read nStr :: Int
                grid = take n rest
            putStrLn (solve grid 0 0 n)