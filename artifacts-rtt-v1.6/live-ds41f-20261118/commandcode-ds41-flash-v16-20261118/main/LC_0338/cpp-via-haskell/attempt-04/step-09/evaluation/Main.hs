module Main where

ones :: Int -> Int
ones 0 = 0
ones x = (x `mod` 2) + ones (x `div` 2)

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (s:_) -> do
            let n = read s :: Int
                counts = map ones [0..n]
            putStrLn (unwords (map show counts))