import System.IO

main :: IO ()
main = do
    hSetBuffering stdin LineBuffering
    n <- readLn :: IO Int
    a <- map read . words <$> getLine :: IO [Int]
    let cur = maximum $ scanl (+) 0 (zipWith max a (drop 1 a))
        best = maximum $ scanl (+) 0 (zipWith max a (drop 1 a))
    print best