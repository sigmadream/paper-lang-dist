module Main where

main :: IO ()
main = do
    input <- getContents
    let (m:n:_) = map read (words input) :: [Int]
        initial = replicate n 1 :: [Integer]
        answer = last $ foldl (\row _ -> tail (scanl (+) 0 row)) initial [1..m-1]
    print answer