{-# LANGUAGE BangPatterns #-}
import Data.Bits
search mask columns down up
  | columns == mask = 1
  | otherwise = choices (mask .&. complement (columns .|. down .|. up)) 0
  where
    choices 0 !count = count
    choices available !count = let bit = available .&. negate available
                                  next = search mask (columns .|. bit) ((down .|. bit) `shiftL` 1) ((up .|. bit) `shiftR` 1)
                              in choices (available-bit) (count+next)
main = do
  n <- fmap read getContents :: IO Int
  let mask = (1 `shiftL` n)-1 :: Int
      branch column = let b = 1 `shiftL` column in search mask b (b `shiftL` 1) (b `shiftR` 1)
  print (2 * sum [branch c | c <- [0..n `div` 2-1]] + if odd n then branch (n `div` 2) else 0)
