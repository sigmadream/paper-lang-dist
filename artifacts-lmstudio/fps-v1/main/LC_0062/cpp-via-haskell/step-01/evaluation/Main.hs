main :: IO ()
main = do
    [m, n] <- map read . words <$> getLine
    let dp = take n (iterate (\row -> zipWith (+) row (tail row)) (replicate n 1))
    print $ last (dp !! (m-1))