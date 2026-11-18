module Main (main) where

import Data.Char (isDigit, isSpace)

main :: IO ()
main = do
  mLine <- getLine'
  let n = case mLine of
            Nothing -> 0
            Just line ->
              let trimmed = dropWhile (== ' ') line
                  digits = takeWhile isDigit trimmed
              in if null digits then 0 else read digits
      cnts = 0 : [ (cnts !! (k `div` 2)) + fromIntegral (k `mod` 2) | k <- [1 .. n] ]
  putStrLn (unwords (map show (take (n + 1) cnts)))

getLine' :: IO (Maybe String)
getLine' = do
  done <- isEOF
  if done then return Nothing else Just return getLine