module Main (main) where

import Data.List (intercalate)
import System.IO

main :: IO ()
main = do
  hSetEncoding stdin utf8
  contents <- getContents
  case words contents of
    (nStr : rest) -> do
      let xs = take (read nStr :: Int) (map read rest :: [Integer])
          nonZeros = filter (/= 0) xs
          zeros = length xs - length nonZeros
          out = nonZeros ++ replicate zeros 0
      putStrLn (intercalate " " (map show out))
    _ -> return ()