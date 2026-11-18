module Main where

main :: IO ()
main = do
    input <- getContents
    case (map read (words input) :: [Int]) of
        [] -> return ()
        (n:xs) -> do
            let arr = take n xs
                result = filter (/= 0) arr ++ filter (== 0) arr
            putStrLn (unwords (map show result))