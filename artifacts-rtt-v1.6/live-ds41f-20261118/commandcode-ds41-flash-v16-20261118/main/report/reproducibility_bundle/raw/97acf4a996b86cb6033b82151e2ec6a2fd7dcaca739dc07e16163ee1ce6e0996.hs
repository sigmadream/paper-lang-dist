import Data.Bits

main :: IO ()
main = do
  input <- getContents
  let n = read (head (words input)) :: Int
      full = (1 `shiftL` n) - 1

      solve r cols d1 d2
        | r == n = 1
        | otherwise =
            let avail = full .&. complement (cols .|. d1 .|. d2)
                go a acc
                  | a == 0 = acc
                  | otherwise =
                      let bit = a .&. (-a)
                          rest = a .&. (a - 1)
                          nextCols = cols .|. bit
                          nextD1 = (d1 .|. bit) `shiftL` 1
                          nextD2 = (d2 .|. bit) `shiftR` 1
                      in go rest (acc + solve (r + 1) nextCols nextD1 nextD2)
            in go avail 0

  print (solve 0 0 0 0)