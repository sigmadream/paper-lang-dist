module Main (main) where

gcd' :: Integer -> Integer -> Integer
gcd' a 0 = a
gcd' a b = gcd' b (a `mod` b)

main :: IO ()
main = do
    inp <- getContents
    case map read (words inp) :: [Integer] of
        (a:b:_) -> do
            let g = gcd' a b
            print g
            print ((a `div` g) * b)
        _ -> return ()