module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getLine
  let ws = words inp
  case ws of
    (ms:ns:_) | Just m <- readMaybeInt ms, Just n <- readMaybeInt ns ->
      putStrLn (show (uniquePaths m n))
    _ -> return ()

uniquePaths :: Integer -> Integer -> Integer
uniquePaths m n = last (foldl' step (replicate (fromInteger n) 1) [2..m])
  where
    step row _ = scanl1 (+) row

readMaybeInt :: String -> Maybe Integer
readMaybeInt s = case reads s of
  [(v, "")] -> Just v
  _         -> Nothing