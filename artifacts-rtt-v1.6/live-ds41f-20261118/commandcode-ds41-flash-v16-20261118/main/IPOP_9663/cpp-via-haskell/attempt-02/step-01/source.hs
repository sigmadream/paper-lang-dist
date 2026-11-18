import Data.Bits (shiftL, shiftR, (.&.), (.|.), xor, complement)

main :: IO ()
main = do
  input <- getContents
  case words input of
    (x:_) -> print (solve (read x :: Int))
    _ -> return ()

solve :: Int -> Int
solve n = go 0 0 0 0
  where
    full = (1 `shiftL` n) - 1 :: Int

    go :: Int -> Int -> Int -> Int -> Int
    go r cols d1 d2
      | r == n = 1
      | otherwise = loop (full .&. complement (cols .|. d1 .|. d2)) 0
      where
        loop :: Int -> Int -> Int
        loop 0 acc = acc
        loop avail acc =
          let b = avail .&. (-avail)
              avail' = avail `xor` b
              acc' = acc + go (r + 1)
                             (cols .|. b)
                             (((d1 .|. b) `shiftL` 1) .&. full)
                             ((d2 .|. b) `shiftR` 1)
          in acc' `seq` loop avail' acc'