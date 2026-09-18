import Data.List (sort)

main :: IO ()
main = do
  n <- readLn :: IO Int
  xs <- map read . words <$> getLine :: IO [Int]
  print $ sort xs