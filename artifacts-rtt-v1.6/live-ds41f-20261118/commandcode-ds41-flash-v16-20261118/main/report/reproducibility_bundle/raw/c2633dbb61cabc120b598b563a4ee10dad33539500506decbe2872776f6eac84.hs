module Main where

main :: IO ()
main = do
    input <- getContents
    let (m:n:_) = map read (words input) :: [Integer]
        row = foldl (\r _ -> scanl1 (+) r) (replicate (fromIntegral n) 1) [2..m]
    print (row !! (fromIntegral n - 1))