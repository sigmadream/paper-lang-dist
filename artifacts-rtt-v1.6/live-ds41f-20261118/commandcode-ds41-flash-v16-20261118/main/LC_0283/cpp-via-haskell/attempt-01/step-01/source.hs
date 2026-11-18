module Main where

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        [] -> return ()
        (nStr:rest) -> do
            let n = read nStr :: Int
                nums = map read (take n rest) :: [Int]
                nonZeros = filter (/= 0) nums
                zeros = replicate (length nums - length nonZeros) 0
                result = nonZeros ++ zeros
            putStrLn (unwords (map show result))