module Main (main) where

import Data.List (intercalate)
import System.Exit (exitSuccess)

main :: IO ()
main = do
  inp <- getContents
  case lines inp of
    (nLine : rest) -> do
      let ns = map read (words (unwords rest)) :: [Integer]
          nonZeros = filter (/= 0) ns
          n = read nLine :: Int
          result = nonZeros ++ replicate (n - length nonZeros) 0
      if null result
        then putStrLn ""
        else putStrLn (intercalate " " (map show result))
    _ -> return ()