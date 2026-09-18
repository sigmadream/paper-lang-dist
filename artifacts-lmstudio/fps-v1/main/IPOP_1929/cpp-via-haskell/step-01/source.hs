import Data.List

main :: IO ()
main = do
    [m, n] <- map read . words <$> getLine
    let primes = sieveOfEratosthenes n
    putStr $ unlines $ show <$> filter (>= m) primes

sieveOfEratosthenes :: Int -> [Int]
sieveOfEratosthenes n = go [2..n] []
  where
    go [] _ = []
    go (p:xs) ps = p : go (filter (\x -> x `mod` p /= 0) xs) (p:ps)