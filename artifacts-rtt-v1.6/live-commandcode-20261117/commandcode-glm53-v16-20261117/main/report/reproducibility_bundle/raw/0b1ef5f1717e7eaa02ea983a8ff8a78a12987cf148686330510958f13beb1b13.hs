module Main (main) where

import Data.List (intercalate)
import System.Exit (exitSuccess)

main :: IO ()
main = do
  input <- getContents
  case lines input of
    (nLine : rest) | Just _ <- readMaybeInt nLine ->
      let nums = concatMap words rest
          a = map readInt nums
          nonZeros = filter (/= 0) a
          zeros = filter (== 0) a
          result = nonZeros ++ zeros
      in putStrLn (intercalate " " (map show result))
    _ -> return ()

readMaybeInt :: String -> Maybe Int
readMaybeInt s = case reads s of
  [(x, _)] -> Just x
  _        -> Nothing

readInt :: String -> Integer
readInt s = case reads s of
  [(x, _)] -> x
  _        -> 0