module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getLine
  let ws = words inp
  case ws of
    (ms:ns:_) -> do
      let m = read ms :: Integer
          n = read ns :: Integer
      print (paths m n)

paths :: Integer -> Integer -> Integer
paths m n = go (replicate (fromIntegral n) 1) (fromIntegral m - 1)
  where
    go dp 0 = dp !! (fromIntegral n - 1)
    go dp k = go (step dp) (k - 1)
    step dp = 1 : tail (scanl1 (+) dp)