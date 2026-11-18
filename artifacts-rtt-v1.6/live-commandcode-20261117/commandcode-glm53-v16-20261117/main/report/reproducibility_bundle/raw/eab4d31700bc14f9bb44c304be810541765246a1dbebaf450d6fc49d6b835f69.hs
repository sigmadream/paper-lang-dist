module Main (main) where

import Data.List (foldl')

valid :: String -> Bool
valid s = go 0 s
  where
    go _ [] = True
    go b (c:cs)
      | b < 0 = False
      | c == '(' = go (b+1) cs
      | otherwise = go (b-1) cs

main :: IO ()
main = do
  contents <- getContents
  let (first:rest) = lines contents
      t = read first :: Int
      inputs = take t rest
      results = map (\s -> if valid s then "YES" else "NO") inputs
  mapM_ putStrLn results