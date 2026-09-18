module Main where

main :: IO ()
main = do
    n <- readLn :: IO Int
    scores <- replicateM n readLn :: IO [Int]
    let dp = calculateDP scores
    print $ dp !! (n - 1)

calculateDP :: [Int] -> [Int]
calculateDP scores = dp
  where
    n = length scores
    dp = foldl' updateDP (replicate n 0) [1..n]
    updateDP dp' i
      | i == 1 = take (i + 1) $ zipWith (+) dp' scores
      | i == 2 = take (i + 1) $ zipWith (+) (zipWith (+) dp' scores) (tail scores)
      | otherwise = take (i + 1) $ zipWith (+) (zipWith max (drop 2 dp') (zipWith (+) (drop 3 dp') (init scores))) (drop i scores)