module Main where

main :: IO ()
main = do
    input <- getContents
    let xs = map read (words input) :: [Int]
    case xs of
        [] -> return ()
        (n:rest) ->
            let arr = take n rest
                nonZeroes = filter (/= 0) arr
                zeroCount = length arr - length nonZeroes
                result = nonZeroes ++ replicate zeroCount 0
            in putStrLn (unwords (map show result))