module Main where

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size
    | allSame   = [first]
    | otherwise = "(" ++ tl ++ tr ++ bl ++ br ++ ")"
  where
    first = (grid !! r) !! c
    allSame = all (\i -> all (\j -> (grid !! i) !! j == first) [c .. c + size - 1]) [r .. r + size - 1]
    half = size `div` 2
    tl = solve grid r c half
    tr = solve grid r (c + half) half
    bl = solve grid (r + half) c half
    br = solve grid (r + half) (c + half) half

main :: IO ()
main = do
    input <- getContents
    let (nLine : gridLines) = lines input
        n = read nLine :: Int
        grid = take n gridLines
    putStrLn (solve grid 0 0 n)