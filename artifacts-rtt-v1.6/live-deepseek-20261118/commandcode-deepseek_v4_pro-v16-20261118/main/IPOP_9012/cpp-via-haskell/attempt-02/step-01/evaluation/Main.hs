module Main where

import System.IO

main :: IO ()
main = do
    contents <- getContents
    let ws = words contents
    let t = read (head ws) :: Int
        strs = take t (tail ws)
        results = map check strs
    putStr $ unlines $ map (\b -> if b then "YES" else "NO") results

check :: String -> Bool
check s = go 0 s
  where
    go bal [] = bal == 0
    go bal (c:cs)
        | bal < 0 = False
        | c == '(' = go (bal + 1) cs
        | c == ')' = go (bal - 1) cs
        | otherwise = False