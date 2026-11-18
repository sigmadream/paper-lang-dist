module Main where

popCount :: Int -> Int
popCount x = go x 0
  where
    go 0 c = c
    go y c = go (y `div` 2) (c + y `mod` 2)

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> return ()
    (s:_) -> do
      let n = read s :: Int
      putStrLn $ unwords $ map (show . popCount) [0..n]