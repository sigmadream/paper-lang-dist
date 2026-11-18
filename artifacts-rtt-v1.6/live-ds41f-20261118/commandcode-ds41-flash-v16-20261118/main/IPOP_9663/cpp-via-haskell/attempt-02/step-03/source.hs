module Main where

import Data.Bits

main :: IO ()
main = do
  s <- getContents
  case reads s :: [(Int, String)] of
    [(n, _)] -> print (solve n)
    _ -> return ()

solve :: Int -> Int
solve n = go 0 0 0 0
  where
    full = (1 `shiftL` n) - 1

    go r cols d1 d2
      | r == n = 1
      | otherwise =
          sum
            [ go
                (r + 1)
                (cols .|. b)
                (((d1 .|. b) `shiftL` 1) .&. full)
                ((d2 .|. b) `shiftR` 1)
            | b <- bitList (full .&. complement (cols .|. d1 .|. d2))
            ]

bitList :: Int -> [Int]
bitList 0 = []
bitList x =
  let b = x .&. negate x
  in b : bitList (x `xor` b)