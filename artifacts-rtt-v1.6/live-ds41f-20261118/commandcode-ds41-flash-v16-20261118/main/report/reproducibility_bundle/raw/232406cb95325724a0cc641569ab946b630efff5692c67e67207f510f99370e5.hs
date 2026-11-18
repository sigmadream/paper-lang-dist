module Main where

import Data.Char (isDigit)
import Data.List (foldl')

parseIntegerLike :: String -> Maybe Integer
parseIntegerLike [] = Nothing
parseIntegerLike s@(c:cs) =
  let (neg, ds) = case c of
        '+' -> (False, cs)
        '-' -> (True, cs)
        _   -> (False, s)
  in if null ds || not (all isDigit ds)
       then Nothing
       else let v = foldl' (\acc d -> acc * 10 + toInteger (fromEnum d - fromEnum '0')) 0 ds
            in Just (if neg then -v else v)

collectNums :: Integer -> [String] -> [Integer]
collectNums k = go k
  where
    go 0 _ = []
    go _ [] = []
    go m (x:xs) =
      case parseIntegerLike x of
        Nothing -> []
        Just v -> v : go (m - 1) xs

maxSubarray :: [Integer] -> Integer
maxSubarray [] = 0
maxSubarray (x:xs) =
  snd (foldl' step (x, x) xs)
  where
    step (cur, best) y =
      let cur' = max y (cur + y)
          best' = max best cur'
      in (cur', best')

main :: IO ()
main = do
  input <- getContents
  let toks = words input
  case toks of
    [] -> return ()
    (t:ts) ->
      case parseIntegerLike t of
        Nothing -> return ()
        Just n -> do
          let k | n <= 0 = 0
                | n > 2147483647 = 2147483647
                | otherwise = n
              nums = collectNums k ts
          print (maxSubarray nums)