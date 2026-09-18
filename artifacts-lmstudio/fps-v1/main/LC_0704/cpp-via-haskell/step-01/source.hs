import System.IO

main :: IO ()
main = do
    hSetBuffering stdin NoBuffering
    hSetBuffering stdout NoBuffering
    [n, target] <- map read . words <$> getLine
    a <- map read . words <$> getLine
    let result = binarySearch 0 n target a
    print result

binarySearch :: Int -> Int -> Int -> [Int] -> Int
binarySearch lo hi target a
    | lo >= hi    = -1
    | otherwise   = case mid of
        m | a !! m < target -> binarySearch (m + 1) hi target a
          | a !! m > target -> binarySearch lo m target a
          | otherwise       -> m
    where
        mid = lo + (hi - lo) `div` 2