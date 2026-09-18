module Main where

uniquePaths :: Int -> Int -> Int
uniquePaths m n = table !! (m-1) !! (n-1)
  where
    table = [[if i == 0 || j == 0 then 1 else table !! (i-1) !! j + table !! i !! (j-1) | j <- [0..n-1]] | i <- [0..m-1]]

main :: IO ()
main = do
  m <- readLn :: IO Int
  n <- readLn :: IO Int
  print $ uniquePaths m n