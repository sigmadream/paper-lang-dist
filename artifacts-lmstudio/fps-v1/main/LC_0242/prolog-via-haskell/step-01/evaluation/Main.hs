import Data.List (sort)
import System.IO

readWords :: IO [String]
readWords = do
  s <- getLine
  t <- getLine
  return [s, t]

frequencies :: String -> [(Char, Int)]
frequencies s = map (\c -> (c, length $ filter (== c) s)) ['a'..'z']

main :: IO ()
main = do
  words <- readWords
  let (s:t:_) = words
  let fa = frequencies s
  let fb = frequencies t
  if fa == fb then putStrLn "1" else putStrLn "0"