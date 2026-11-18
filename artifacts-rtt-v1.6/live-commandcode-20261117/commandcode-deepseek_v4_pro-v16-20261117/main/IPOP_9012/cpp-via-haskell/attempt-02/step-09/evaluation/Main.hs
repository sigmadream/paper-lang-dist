module Main where

import Control.Monad (replicateM)

isValid :: String -> Bool
isValid = go 0
  where
    go bal [] = bal == 0
    go bal (c:cs)
      | c == '(' = go (bal + 1) cs
      | c == ')' = bal > 0 && go (bal - 1) cs
      | otherwise = False

main :: IO ()
main = do
  tStr <- getLine
  let t = read tStr :: Int
  strings <- replicateM t getLine
  mapM_ (\s -> putStrLn (if isValid s then "YES" else "NO")) strings