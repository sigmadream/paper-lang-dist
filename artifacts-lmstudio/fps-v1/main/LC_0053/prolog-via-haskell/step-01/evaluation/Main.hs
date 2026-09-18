import Data.List (foldl')

kadane :: [Int] -> Int
kadane xs = snd $ foldl' (\(maxSoFar, maxEndingHere) x -> 
    let maxEndingHere' = max x (maxEndingHere + x)
        maxSoFar' = max maxSoFar maxEndingHere'
    in (maxSoFar', maxEndingHere')) (0, 0) xs

main :: IO ()
main = do
    n <- readLn :: IO Int
    nums <- map read . words <$> getLine :: IO [Int]
    print $ kadane (drop 1 nums)