module Main (main) where

import Data.List (intercalate)

main :: IO ()
main = do
  inp <- getLine
  let n = read inp :: Int
  if n < 0
    then return ()
    else do
      let arr = 0 : go 1
          go i
            | i > n = []
            | otherwise = (arr !! (i `div` 2) + i `mod` 2) : go (i + 1)
      putStrLn $ intercalate " " (map show arr)