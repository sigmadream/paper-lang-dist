module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getContents
  case map read (words inp) of
    (m:n:_) -> print (paths m n)
    _ -> return ()
  where
    paths m n = last (foldl' step (replicate n 1) [2..m])
    step dp _ = scanl1 (+) dp