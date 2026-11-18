module Main (main) where

import Data.List (intercalate)
import System.Exit (exitSuccess)

main :: IO ()
main = do
  inp <- getContents
  case lines inp of
    (nLine:rest) -> do
      let ns = map read (words (unwords rest)) :: [Integer]
          nonZeros = filter (/= 0) ns
          zeros = length ns - length nonZeros
          out = nonZeros ++ replicate zeros 0
      putStrLn (intercalate " " (map show out))
    _ -> exitSuccess