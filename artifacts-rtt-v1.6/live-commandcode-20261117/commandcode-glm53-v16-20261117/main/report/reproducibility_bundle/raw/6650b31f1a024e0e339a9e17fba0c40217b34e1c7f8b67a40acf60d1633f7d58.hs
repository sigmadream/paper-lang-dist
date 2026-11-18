module Main (main) where

import Data.List (intercalate)
import System.Exit (exitSuccess)

main :: IO ()
main = do
  input <- getContents
  case mapM readMaybeInt (words input) of
    Nothing -> exitSuccess
    Just xs -> case xs of
      (n:rest) -> do
        let a = take n rest
            nonZeros = filter (/= 0) a
            result = nonZeros ++ replicate (n - length nonZeros) 0
        putStrLn (intercalate " " (map show result))
      _ -> return ()

readMaybeInt :: String -> Maybe Int
readMaybeInt s = case reads s of
  [(x, "")] -> Just x
  _ -> Nothing