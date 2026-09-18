import System.IO

main :: IO ()
main = do
    hSetBuffering stdin LineBuffering
    hSetBuffering stdout NoBuffering
    [a, b] <- map read . words <$> getLine
    let g = gcd a b
    putStrLn $ show g
    putStrLn $ show ((a `div` g) * b)