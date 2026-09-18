import Data.List

main :: IO ()
main = do
  n <- readLn :: IO Int
  xs <- replicateM n readLn :: IO [Int]
  let sortedXs = sort xs
  if hasDuplicate sortedXs then putStrLn "1" else putStrLn "0"

hasDuplicate :: Ord a => [a] -> Bool
hasDuplicate [] = False
hasDuplicate [_] = False
hasDuplicate (x:y:xs)
  | x == y    = True
  | otherwise = hasDuplicate (y:xs)