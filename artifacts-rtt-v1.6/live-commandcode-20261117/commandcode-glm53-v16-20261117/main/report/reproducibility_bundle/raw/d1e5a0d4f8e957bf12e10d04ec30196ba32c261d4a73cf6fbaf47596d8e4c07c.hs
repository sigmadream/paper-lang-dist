module Main (main) where

import Data.List (intercalate)
import System.Exit (exitSuccess)

main :: IO ()
main = do
  inp <- getContents
  case lines inp of
    (nLine : rest) | (n, _) : _ <- reads nLine ->
      let nums = take n (map read (concatMap words rest) :: [Integer])
          nonZeros = filter (/= 0) nums
          zeros = replicate (n - length nonZeros) 0
      in putStrLn (intercalate " " (map show (nonZeros ++ zeros)))
    _ -> return ()