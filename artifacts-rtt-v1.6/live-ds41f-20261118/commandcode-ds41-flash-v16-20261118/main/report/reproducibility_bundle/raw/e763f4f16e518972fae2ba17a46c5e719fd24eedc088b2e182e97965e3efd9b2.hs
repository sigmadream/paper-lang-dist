module Main where

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        [] -> return ()
        (nToken:rest) -> do
            let n = read nToken :: Int
                xs = map read (take n rest) :: [Int]
                nonZeros = filter (/= 0) xs
                zeroCount = length xs - length nonZeros
                result = nonZeros ++ replicate zeroCount 0
            putStrLn (unwords (map show result))