module Main where

main :: IO ()
main = do
  input <- getContents
  let (m:n:_) = map read (words input) :: [Integer]
      dp = foldl (\row _ -> scanl1 (+) row) (replicate (fromIntegral n) 1) [2..m]
  print (last dp)