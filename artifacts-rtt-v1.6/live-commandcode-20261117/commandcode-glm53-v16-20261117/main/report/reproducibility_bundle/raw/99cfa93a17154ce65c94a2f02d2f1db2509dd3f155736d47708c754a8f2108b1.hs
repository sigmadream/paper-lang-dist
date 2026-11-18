module Main (main) where

import System.IO

main :: IO ()
main = do
  contents <- getContents
  let (tLine : rest) = lines contents
      t = read tLine :: Int
      cases = take t rest
  mapM_ (putStrLn . result) cases
  where
    result s = if valid s then "YES" else "NO"
    valid s = go 0 s
    go _ [] = True
    go bal (c:cs)
      | c == '(' = go (bal+1) cs
      | otherwise = bal > 0 && go (bal-1) cs