module Main where

main :: IO ()
main = do
  input <- getContents
  let values = map read (words input) :: [Int]
  case values of
    (m:n:_) -> print (uniquePaths m n)
    _ -> return ()

uniquePaths :: Int -> Int -> Int
uniquePaths m n = last ((iterate (scanl1 (+)) (replicate n 1)) !! (m - 1))