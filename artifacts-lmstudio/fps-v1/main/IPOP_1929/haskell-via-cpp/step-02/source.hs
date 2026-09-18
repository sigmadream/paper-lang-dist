module Main where

main :: IO ()
main = do
    [lo, hi] <- map read . words <$> getLine
    mapM_ print $ filter isPrime [lo..hi]

isPrime :: Int -> Bool
isPrime n
    | n < 2     = False
    | otherwise = all (\d -> n `mod` d /= 0) [2..(floor . sqrt . fromIntegral $ n)]