module Main where

main :: IO ()
main = do
    input <- getContents
    let values = map read (words input) :: [Integer]
    case values of
        (n:rest) ->
            let arr = take (fromIntegral n) rest
                nonZeros = filter (/= 0) arr
                zeros = replicate (fromIntegral n - length nonZeros) 0
            in putStrLn (unwords (map show (nonZeros ++ zeros)))
        [] -> pure ()