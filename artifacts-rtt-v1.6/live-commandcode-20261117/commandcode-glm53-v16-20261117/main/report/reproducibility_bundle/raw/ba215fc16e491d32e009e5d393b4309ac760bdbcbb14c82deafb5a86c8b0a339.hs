module Main (main) where

import Data.List (intercalate)
import System.Exit (exitSuccess)

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> return ()
    (nStr:rest) -> do
      let n = read nStr :: Int
          a = map read (take n rest) :: [Integer]
          nonZeros = filter (/= 0) a
          result = nonZeros ++ replicate (n - length nonZeros) 0
      putStrLn (intercalate " " (map show result))