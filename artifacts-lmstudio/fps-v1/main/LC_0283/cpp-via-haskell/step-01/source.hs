import System.IO

main :: IO ()
main = do
    hSetBuffering stdin LineBuffering
    n <- readLn :: IO Int
    a <- map read . words <$> getLine :: IO [Int]
    let write = go 0 a where
            go i [] = []
            go i (x:xs)
                | x /= 0    = x : go (i+1) xs
                | otherwise = go i xs
    print $ write ++ replicate (n - length write) 0