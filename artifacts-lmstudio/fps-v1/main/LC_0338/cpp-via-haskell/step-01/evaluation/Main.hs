main :: IO ()
main = do
    n <- readLn :: IO Int
    let counts = [countBits x | x <- [0..n]]
    mapM_ print counts

countBits :: Int -> Int
countBits x = go x 0
  where
    go 0 acc = acc
    go n acc = go (n `div` 2) (acc + n `mod` 2)