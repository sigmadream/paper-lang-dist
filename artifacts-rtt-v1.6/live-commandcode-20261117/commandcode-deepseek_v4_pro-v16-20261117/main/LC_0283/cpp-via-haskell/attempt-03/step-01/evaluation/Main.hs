module Main where

main :: IO ()
main = do
    content <- getContents
    let tokens = words content
        n = read (head tokens) :: Int
        xs = map read (take n (tail tokens)) :: [Int]
        nonzeros = filter (/= 0) xs
        zeros = filter (== 0) xs
        result = nonzeros ++ zeros
    putStrLn (unwords (map show result))