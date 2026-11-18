module Main where

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (x:xs) -> do
            let n = read x :: Int
                grid = take n xs
            putStrLn (solve grid 0 0 n)

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size =
    let first = (grid !! r) !! c
        same = and [ (grid !! i) !! j == first
                   | i <- [r .. r + size - 1]
                   , j <- [c .. c + size - 1]
                   ]
    in if same
         then [first]
         else
           let half = size `div` 2
               topLeft = solve grid r c half
               topRight = solve grid r (c + half) half
               bottomLeft = solve grid (r + half) c half
               bottomRight = solve grid (r + half) (c + half) half
           in "(" ++ topLeft ++ topRight ++ bottomLeft ++ bottomRight ++ ")"