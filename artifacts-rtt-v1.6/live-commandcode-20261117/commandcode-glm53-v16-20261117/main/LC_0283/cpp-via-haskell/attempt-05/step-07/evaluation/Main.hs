module Main (main) where

import Data.List (intercalate)
import System.IO

main :: IO ()
main = do
  inp <- getContents
  let ws = words inp
  case ws of
    (nStr:rest) -> do
      let n = read nStr :: Int
          xs = take n (map read rest) :: [Integer]
          nonZeros = filter (/= 0) xs
          zeros = filter (== 0) xs
          result = nonZeros ++ zeros
      putStrLn (intercalate " " (map show result))
    _ -> return ()