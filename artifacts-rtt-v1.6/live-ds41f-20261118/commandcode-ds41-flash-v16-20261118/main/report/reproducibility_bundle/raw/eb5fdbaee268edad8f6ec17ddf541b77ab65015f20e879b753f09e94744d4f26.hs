module Main where

popCount :: Int -> Int
popCount x = go x 0
  where
    go 0 acc = acc
    go y acc = go (y `div` 2) (acc + y `mod` 2)

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (s:_) -> do
            let n = read s :: Int
            putStrLn (unwords (map (show . popCount) [0..n]))