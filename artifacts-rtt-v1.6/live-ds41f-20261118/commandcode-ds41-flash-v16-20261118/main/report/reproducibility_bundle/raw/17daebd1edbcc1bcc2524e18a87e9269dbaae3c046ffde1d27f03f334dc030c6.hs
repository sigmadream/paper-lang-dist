module Main where

popCount :: Int -> Int
popCount 0 = 0
popCount x = x `mod` 2 + popCount (x `div` 2)

main :: IO ()
main = do
    input <- getContents
    let n = read (head (words input)) :: Int
    putStrLn $ unwords $ map (show . popCount) [0..n]