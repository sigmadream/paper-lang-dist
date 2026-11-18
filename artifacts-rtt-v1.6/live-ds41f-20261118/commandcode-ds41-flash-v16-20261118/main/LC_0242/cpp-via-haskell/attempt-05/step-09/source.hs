module Main where

import Data.List (sort)

isCWhitespace :: Char -> Bool
isCWhitespace c =
  c == ' ' || c == '\t' || c == '\n' ||
  c == '\v' || c == '\f' || c == '\r'

stripTrailing :: String -> String
stripTrailing = reverse . dropWhile isCWhitespace . reverse

main :: IO ()
main = do
  input <- getContents
  let lns = lines input
  case lns of
    [] -> return ()
    [_] -> putStr "0\n"
    (s:t:_) -> do
      let s' = stripTrailing s
          t' = stripTrailing t
      putStrLn (if sort s' == sort t' then "1" else "0")