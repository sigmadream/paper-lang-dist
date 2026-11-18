module Main (main) where

import System.IO

gcd' :: Integer -> Integer -> Integer
gcd' a b
  | b == 0    = a
  | otherwise = gcd' b (a `mod` b)

main :: IO ()
main = do
  inp <- getLine
  let ws = words inp
  case ws of
    (aStr:bStr:_) | Just a <- readInt aStr, Just b <- readInt bStr ->
      let g = gcd' a b
      in putStrLn (show g) >> putStrLn (show ((a `div` g) * b))
    _ -> return ()
  where
    readInt s = case s of
      '+':rest -> readInt rest
      _ -> case reads s of
             [(n, "")] -> Just n
             _         -> Nothing