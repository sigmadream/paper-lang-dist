module Main (main) where

import Data.List (intercalate)
import System.Exit

main :: IO ()
main = do
  inp <- getContents
  let ws = words inp
  case ws of
    (nStr:rest) -> do
      let n = read nStr :: Int
          xs = take n (map read rest :: [Integer])
          nonZeros = filter (/= 0) xs
          zeros = replicate (n - length nonZeros) 0
          res = nonZeros ++ zeros
      putStrLn (unwords (map show res))
    _ -> return ()