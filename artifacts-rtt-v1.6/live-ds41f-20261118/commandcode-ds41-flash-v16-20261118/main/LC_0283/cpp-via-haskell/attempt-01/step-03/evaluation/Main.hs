module Main where

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        [] -> return ()
        (nStr : rest) ->
            let n = read nStr :: Int
                nums = map read (take n rest) :: [Int]
                nonZeros = filter (/= 0) nums
                zeros = replicate (n - length nonZeros) 0
                result = nonZeros ++ zeros
            in putStrLn (unwords (map show result))