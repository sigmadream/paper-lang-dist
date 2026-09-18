import System.IO

gcd' :: Int -> Int -> Int
gcd' a b
  | b == 0    = a
  | otherwise = gcd' b (a `mod` b)

main :: IO ()
main = do
  hSetBuffering stdin NoBuffering
  hSetBuffering stdout NoBuffering
  [a, b] <- map read . words <$> getLine
  let g = gcd' a b
  putStrLn $ show g
  putStrLn $ show ((a `div` g) * b)