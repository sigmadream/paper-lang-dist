module Main where

import Data.Array (Array, listArray, (!))

parseToken :: String -> Int
parseToken s =
  let (sign, rest) = case s of
        [] -> (1, "")
        ('+':xs) -> (1, xs)
        ('-':xs) -> (-1, xs)
        _ -> (1, s)
  in if null rest then 0 else go sign rest 0
  where
    limit = 2147483648 :: Integer

    go :: Integer -> String -> Integer -> Int
    go sg [] val = finish sg val
    go sg (c:cs) val
      | c < '0' || c > '9' = 0
      | otherwise =
          let nv = val * 10 + toInteger (fromEnum c - fromEnum '0')
          in if nv > limit then 0 else go sg cs nv

    finish :: Integer -> Integer -> Int
    finish sg val =
      let v = sg * val
      in if v < -2147483648 || v > 2147483647 then 0 else fromInteger v

main :: IO ()
main = do
  input <- getContents
  let token = case words input of
                (x:_) -> x
                [] -> ""
      n0 = parseToken token
      n = if n0 < 0 then 0 else n0

      counts :: Array Int Int
      counts = listArray (0, n) [f i | i <- [0..n]]

      f 0 = 0
      f i = counts ! (i `div` 2) + (i `mod` 2)

      answer = unwords [show (counts ! i) | i <- [0..n]]
  putStrLn answer