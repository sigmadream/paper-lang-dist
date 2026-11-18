module Main where

import Data.Array (listArray, (!))

parseToken :: String -> Int
parseToken s =
  let (sign, rest) =
        case s of
          [] -> (1, "")
          ('+':xs) -> (1, xs)
          ('-':xs) -> (-1, xs)
          _ -> (1, s)
  in if null rest
       then 0
       else case parseDigits rest of
              Nothing -> 0
              Just val ->
                let v = sign * val
                in if v < -2147483648 || v > 2147483647
                     then 0
                     else fromInteger v

parseDigits :: String -> Maybe Integer
parseDigits = go 0
  where
    limit = 2147483648 :: Integer

    go v [] = Just v
    go v (c:cs)
      | c < '0' || c > '9' = Nothing
      | otherwise =
          let nv = v * 10 + toInteger (fromEnum c - fromEnum '0')
          in if nv > limit then Nothing else go nv cs

main :: IO ()
main = do
  input <- getContents
  let token = case words input of
                (t:_) -> t
                [] -> ""
      n0 = parseToken token
      n = if n0 < 0 then 0 else n0
      counts = listArray (0, n) [countAt i | i <- [0..n]]
      countAt i
        | i == 0 = 0
        | otherwise = counts ! (i `div` 2) + (i `mod` 2)
  putStrLn (unwords [show (counts ! i) | i <- [0..n]])