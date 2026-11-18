module Main (main) where

import Data.List (intercalate)
import System.Exit

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> return ()
    (nStr:rest) -> do
      let n = read nStr :: Int
          xs = take n (map read rest) :: [Integer]
          nonZeros = filter (/= 0) xs
          result = nonZeros ++ replicate (n - length nonZeros) 0
      putStrLn (intercalate " " (map show result))