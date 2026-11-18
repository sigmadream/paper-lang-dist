module Main (main) where

import Data.Char (isSpace)

main :: IO ()
main = do
  cs <- getContents
  let (tLine : rest) = lines cs
      t = read (trim tLine) :: Int
      ps = take t rest
  mapM_ (putStrLn . judge) ps
  where
    trim = f . f
      where f = reverse . dropWhile isSpace
    judge s = if check 0 s then "YES" else "NO"
    check b [] = b == 0
    check b (c:cs)
      | b < 0 = False
      | c == '(' = check (b+1) cs
      | otherwise = check (b-1) cs