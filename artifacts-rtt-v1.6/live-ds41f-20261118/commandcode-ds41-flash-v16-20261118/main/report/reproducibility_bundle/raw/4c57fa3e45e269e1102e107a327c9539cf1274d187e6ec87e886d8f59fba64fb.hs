module Main where

main :: IO ()
main = do
    input <- getContents
    let ls = lines input
    case ls of
        [] -> return ()
        (nLine:rows) -> do
            let n = read nLine :: Int
                grid = take n rows
            putStrLn (solve grid 0 0 n)

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size =
    let first = (grid !! r) !! c
        same = allSame grid r c size first
    in if same
        then [first]
        else
            let h = size `div` 2
            in "(" ++
               solve grid r c h ++
               solve grid r (c + h) h ++
               solve grid (r + h) c h ++
               solve grid (r + h) (c + h) h ++
               ")"

allSame :: [String] -> Int -> Int -> Int -> Char -> Bool
allSame grid r c size first =
    all (\i -> all (\j -> (grid !! (r + i)) !! (c + j) == first)
                   [0 .. size - 1])
        [0 .. size - 1]