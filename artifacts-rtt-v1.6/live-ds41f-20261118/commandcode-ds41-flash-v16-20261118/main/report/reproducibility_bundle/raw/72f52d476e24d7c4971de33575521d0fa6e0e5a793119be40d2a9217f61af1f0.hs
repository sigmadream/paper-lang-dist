module Main where

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (nStr:rest) -> do
            let n = read nStr :: Int
                grid = take n rest
                ans = solve grid 0 0 n
            putStrLn ans

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size =
    let first = (grid !! r) !! c
        same = all (\i -> all (\j -> (grid !! i) !! j == first)
                             [c .. c + size - 1])
                   [r .. r + size - 1]
    in if same
       then [first]
       else
           let h = size `div` 2
           in "("
              ++ solve grid r c h
              ++ solve grid r (c + h) h
              ++ solve grid (r + h) c h
              ++ solve grid (r + h) (c + h) h
              ++ ")"