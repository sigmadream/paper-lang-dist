import System.IO

gcdValue :: Int -> Int -> Int
gcdValue a 0 = a
gcdValue a b = gcdValue b (a `mod` b)

main :: IO ()
main = do
    [a, b] <- map read . words <$> getLine
    let g = gcdValue a b
        l = (a `div` g) * b
    print g
    print l