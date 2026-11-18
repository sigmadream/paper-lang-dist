module Main where

main :: IO ()
main = do
    input <- getContents
    case map read (words input) :: [Int] of
        [] -> return ()
        (n:rest) -> do
            let nums = take n rest
                nonzero = filter (/= 0) nums
                zeros = replicate (n - length nonzero) 0
            putStrLn (unwords (map show (nonzero ++ zeros)))