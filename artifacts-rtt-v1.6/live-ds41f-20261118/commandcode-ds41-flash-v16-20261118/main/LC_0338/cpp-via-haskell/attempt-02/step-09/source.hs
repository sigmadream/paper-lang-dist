module Main where

import Data.Array (Array, listArray, (!))

parseDigits :: String -> Maybe Integer
parseDigits s
  | null s = Nothing
  | otherwise = go 0 s
  where
    limit = 2147483648
    go v [] = Just v
    go v (c:cs)
      | c < '0' || c > '9' = Nothing
      | otherwise =
          let v' = v * 10 + toInteger (fromEnum c - fromEnum '0')
          in if v' > limit then Nothing else go v' cs

parseToken :: String -> Int
parseToken s =
  case s of
    [] -> 0
    _ ->
      let (sign, rest) =
            case s of
              ('+':xs) -> (1 :: Integer, xs)
              ('-':xs) -> (-1 :: Integer, xs)
              _        -> (1 :: Integer, s)
      in if null rest
           then 0
           else case parseDigits rest of
                  Nothing -> 0
                  Just val ->
                    let v = sign * val
                    in if v < -2147483648 || v > 2147483647
                         then 0
                         else fromInteger v

main :: IO ()
main = do
  input <- getContents
  let token = case words input of
                (x:_) -> x
                []    -> ""
      n0 = parseToken token
      n = if n0 < 0 then 0 else n0
      counts = listArray (0, n)
                 [ if i == 0
                     then 0
                     else counts ! (i `div` 2) + (i `mod` 2)
                 | i <- [0..n]
                 ] :: Array Int Int
      output = unwords [ show (counts ! i) | i <- [0..n] ] ++ "\n"
  putStr output