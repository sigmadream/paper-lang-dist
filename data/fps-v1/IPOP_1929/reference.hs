prime n = n >= 2 && trial 2
  where
    trial d | d*d > n = True
            | n `mod` d == 0 = False
            | otherwise = trial (d+1)
main = do
  [lo,hi] <- fmap (map read . words) getContents :: IO [Int]
  mapM_ print (filter prime [lo..hi])
