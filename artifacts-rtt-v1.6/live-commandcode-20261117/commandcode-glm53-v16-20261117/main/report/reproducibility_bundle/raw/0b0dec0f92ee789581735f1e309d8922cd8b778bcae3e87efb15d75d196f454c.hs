module Main (main) where

import Data.List (intercalate)

main :: IO ()
main = do
  _ <- readLn :: IO Int
  rest <- getContents
  let xs = map read (words rest) :: [Integer]
      nonZeros = filter (/= 0) xs
      zeros = replicate (length xs - length nonZeros) 0
  putStrLn (intercalate " " (map show (nonZeros ++ zeros)))