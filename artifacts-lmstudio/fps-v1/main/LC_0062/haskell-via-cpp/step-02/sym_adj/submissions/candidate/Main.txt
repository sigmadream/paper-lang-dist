module Main where

main :: IO ()
main = do
    [m, n] <- map read . words <$> getLine
    let result = uniquePaths m n
    print result

uniquePaths :: Int -> Int -> Int
uniquePaths m n = table !! (m-1) !! (n-1)
  where
    table = [[if i == 0 || j == 0 then 1 else table !! (i-1) !! j + table !! i !! (j-1) | j <- [0..n]] | i <- [0..m]]