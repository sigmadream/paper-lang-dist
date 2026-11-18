module Main where

main :: IO ()
main = do
    input <- getContents
    let ls = lines input
    case ls of
        (nStr:rest) -> do
            let n = read nStr :: Int
                grid = take n rest
            putStrLn (solve grid 0 0 n)
        _ -> return ()

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size =
    let first = grid !! r !! c
        same = and [ grid !! i !! j == first
                   | i <- [r .. r + size - 1]
                   , j <- [c .. c + size - 1] ]
    in if same
       then [first]
       else let h = size `div` 2
            in "(" ++ solve grid r c h
                   ++ solve grid r (c + h) h
                   ++ solve grid (r + h) c h
                   ++ solve grid (r + h) (c + h) h
                   ++ ")"