import System.IO

main :: IO ()
main = do
    hSetBuffering stdin LineBuffering
    hSetBuffering stdout NoBuffering
    n <- readLn :: IO Int
    xs <- replicateM n (readLn :: IO Int)
    let result = moveZeroes xs
    mapM_ print result

moveZeroes :: [Int] -> [Int]
moveZeroes xs = go 0 xs []
  where
    go _ [] acc = reverse acc
    go i (x:xs) acc
        | x /= 0    = go (i + 1) xs (x : acc)
        | otherwise = go (i + 1) xs acc