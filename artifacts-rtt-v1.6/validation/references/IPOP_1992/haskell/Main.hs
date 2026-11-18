import Data.Array
encode grid r c size
  | all (==first) [grid!(i,j) | i <- [r..r+size-1], j <- [c..c+size-1]] = [first]
  | otherwise = "(" ++ concat [encode grid (r+dr) (c+dc) half | (dr,dc) <- [(0,0),(0,half),(half,0),(half,half)]] ++ ")"
  where first = grid!(r,c)
        half = size `div` 2
main = do
  (size:rows) <- fmap words getContents
  let n = read size :: Int
      grid = listArray ((0,0),(n-1,n-1)) (concat rows)
  putStrLn (encode grid 0 0 n)
