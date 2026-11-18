module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getLine
  case map read (words inp) :: [Integer] of
    (m:n:_) -> print (paths m n)
    _ -> return ()
  where
    paths m n = last $ foldl' step (replicate (fromInteger n) 1) [2 .. m]
    step dp _ = scanl1 (+) dp