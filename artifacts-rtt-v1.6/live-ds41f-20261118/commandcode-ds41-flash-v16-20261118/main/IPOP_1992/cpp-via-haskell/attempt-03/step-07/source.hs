module Main where

solve :: [[Char]] -> Int -> Int -> Int -> String
solve grid r c size =
    let first = (grid !! r) !! c
        same = all (\i -> all (\j -> (grid !! i) !! j == first) [c .. c + size - 1]) [r .. r + size - 1]
    in if same
       then [first]
       else let half = size `div` 2
                topLeft = solve grid r c half
                topRight = solve grid r (c + half) half
                bottomLeft = solve grid (r + half) c half
                bottomRight = solve grid (r + half) (c + half) half
            in "(" ++ topLeft ++ topRight ++ bottomLeft ++ bottomRight ++ ")"

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        [] -> return ()
        (nStr : rest) -> do
            let n = read nStr :: Int
                grid = take n rest
                result = solve grid 0 0 n
            putStrLn result