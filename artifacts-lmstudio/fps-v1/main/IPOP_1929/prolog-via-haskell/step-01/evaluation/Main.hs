import Data.List

isPrime :: Int -> Bool
isPrime n | n < 2     = False
          | otherwise = all (\d -> n `mod` d /= 0) [2..(floor . sqrt $ fromIntegral n)]

main :: IO ()
main = do
    [l, h] <- map read . words <$> getLine
    mapM_ print [n | n <- [l..h], isPrime n]