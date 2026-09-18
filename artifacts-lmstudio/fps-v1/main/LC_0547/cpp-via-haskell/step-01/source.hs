import Data.List (findIndex)

main :: IO ()
main = do
    n <- readLn :: IO Int
    g <- replicateM n (readLine n) :: IO [[Int]]
    let components = countComponents g
    print components

countComponents :: [[Int]] -> Int
countComponents g = go g (replicate (length g) False)
  where
    go [] _ = 0
    go (r:rs) seen
      | any (`notElem` seen) r = 1 + go rs (markSeen r seen)
      | otherwise = go rs seen

markSeen :: [Int] -> [Bool] -> [Bool]
markSeen row seen = zipWith (\x s -> if x == 1 then True else s) row seen