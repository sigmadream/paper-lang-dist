module Main where

counts :: [Int]
counts = 0 : concatMap (\k -> map (+ 1) (take (2 ^ k) counts)) [0 ..]

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (x:_) -> do
            let n = read x :: Int
            putStrLn $ unwords $ map show $ take (n + 1) counts