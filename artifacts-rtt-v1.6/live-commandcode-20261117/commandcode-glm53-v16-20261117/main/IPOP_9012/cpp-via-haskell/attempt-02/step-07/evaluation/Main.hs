module Main (main) where

import System.IO

valid :: String -> Bool
valid = go 0
  where
    go _ [] = True
    go b (c:cs)
      | b' < 0 = False
      | otherwise = go b' cs
      where b' = if c == '(' then b + 1 else b - 1

main :: IO ()
main = do
  contents <- getContents
  let (tLine:rest) = lines contents
      t = read tLine :: Int
      results = map (\s -> if valid s then "YES" else "NO") (take t rest)
  mapM_ putStrLn results