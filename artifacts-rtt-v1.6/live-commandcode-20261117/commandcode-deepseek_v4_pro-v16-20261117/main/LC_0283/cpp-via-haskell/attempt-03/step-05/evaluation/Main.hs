module Main where

main :: IO ()
main = do
    input <- getContents
    let tokens = map read (words input) :: [Int]
        n = head tokens
        nums = take n (tail tokens)
        nonZeros = filter (/= 0) nums
        zeros = filter (== 0) nums
        result = nonZeros ++ zeros
    putStrLn $ unwords $ map show result