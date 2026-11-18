module Main where

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (x:rest) -> do
            let n = read x :: Int
                scores = map read (take n rest) :: [Int]
            print (solve n scores)

solve :: Int -> [Int] -> Int
solve n scores
    | n <= 0 = 0
    | n == 1 = scores !! 0
    | n == 2 = (scores !! 0) + (scores !! 1)
    | otherwise = loop 3 dp2 dp1 0
  where
    s i = scores !! (i - 1)
    dp1 = s 1
    dp2 = dp1 + s 2

    loop i prev1 prev2 prev3
        | i > n = prev1
        | otherwise = loop (i + 1) next prev1 prev2
      where
        next = max prev2 (prev3 + s (i - 1)) + s i