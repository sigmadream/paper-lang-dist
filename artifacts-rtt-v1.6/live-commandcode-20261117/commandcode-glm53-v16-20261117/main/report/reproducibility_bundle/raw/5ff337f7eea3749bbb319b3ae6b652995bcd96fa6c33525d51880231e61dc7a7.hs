import Data.List (sort, foldl')
placed gap (x:xs) = fst (foldl' step (1,x) xs)
  where step (count,previous) house = if house-previous >= gap then (count+1,house) else (count,previous)
search houses needed lo hi answer
  | lo > hi = answer
  | placed mid houses >= needed = search houses needed (mid+1) hi mid
  | otherwise = search houses needed lo (mid-1) answer
  where mid = (lo+hi) `div` 2
main = do
  (_:needed:values) <- fmap (map read . words) getContents :: IO [Int]
  let houses = sort values
  print (search houses needed 1 (last houses-head houses) 0)
