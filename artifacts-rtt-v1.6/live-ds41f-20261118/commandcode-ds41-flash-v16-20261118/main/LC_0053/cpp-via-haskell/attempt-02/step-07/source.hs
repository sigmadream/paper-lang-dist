module Main where

import Text.Read (readMaybe)

parseLL :: String -> Maybe Integer
parseLL s = readMaybe s :: Maybe Integer

takeNums :: Integer -> [String] -> [Integer]
takeNums k _ | k <= 0 = []
takeNums _ [] = []
takeNums k (x:xs) =
  case parseLL x of
    Nothing -> []
    Just v  -> v : takeNums (k - 1) xs

maxSubarray :: [Integer] -> Integer
maxSubarray [] = 0
maxSubarray (x:xs) = go x x xs
  where
    go cur best [] = best
    go cur best (v:vs) =
      let cur'  = max v (cur + v)
          best' = max best cur'
      in go cur' best' vs

main :: IO ()
main = do
  input <- getContents
  let toks = words input
  case toks of
    [] -> return ()
    (t:rest) ->
      case parseLL t of
        Nothing -> return ()
        Just n -> do
          let intMax = 2147483647 :: Integer
              k
                | n <= 0 = 0
                | n > intMax = intMax
                | otherwise = n
              nums = takeNums k rest
          if null nums
            then putStrLn "0"
            else print (maxSubarray nums)