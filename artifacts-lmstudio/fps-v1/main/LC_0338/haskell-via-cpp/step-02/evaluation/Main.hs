countOnes :: Int -> Int
countOnes n = length $ filter (== '1') $ showIntAtBase 2 intToDigit n ""

main :: IO ()
main = do
    n <- readLn :: IO Int
    mapM_ print $ map countOnes [0..n]