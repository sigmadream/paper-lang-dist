module Main where

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size =
    let first = (grid !! r) !! c
        same = all (\i -> all (\j -> (grid !! i) !! j == first) [c .. c + size - 1])
                   [r .. r + size - 1]
    in if same
       then [first]
       else let half = size `div` 2
                tl = solve grid r c half
                tr = solve grid r (c + half) half
                bl = solve grid (r + half) c half
                br = solve grid (r + half) (c + half) half
            in "(" ++ tl ++ tr ++ bl ++ br ++ ")"

main :: IO ()
main = do
    input <- getContents
    let ls = lines input
    case ls of
        [] -> return ()
        (nstr:rest) -> do
            let n = read nstr :: Int
                grid = take n rest
            putStrLn (solve grid 0 0 n)