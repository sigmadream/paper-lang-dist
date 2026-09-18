import Data.Set (Set, empty, insert, member)

main :: IO ()
main = do
    n <- readLn :: IO Int
    a <- replicateM n readLn :: IO [Int]
    let seen = go empty a
    print $ if null seen then 0 else 1
  where
    go :: Set Int -> [Int] -> Set Int
    go s [] = s
    go s (x:xs)
        | x `member` s = s
        | otherwise     = go (insert x s) xs