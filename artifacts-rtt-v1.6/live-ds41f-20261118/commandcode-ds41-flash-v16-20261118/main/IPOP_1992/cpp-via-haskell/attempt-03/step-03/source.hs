module Main where

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size =
    let first = (grid !! r) !! c
        same = all (\i -> all (\j -> (grid !! i) !! j == first) [c .. c + size - 1]) [r .. r + size - 1]
    in if same
        then [first]
        else
            let half = size `div` 2
            in "("
               ++ solve grid r c half
               ++ solve grid r (c + half) half
               ++ solve grid (r + half) c half
               ++ solve grid (r + half) (c + half) half
               ++ ")"

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (nStr:rest) -> do
            let n = read nStr :: Int
                grid = take n rest
            putStrLn (solve grid 0 0 n)