module Main where

main :: IO ()
main = do
    input <- getContents
    let tokens = map read (words input) :: [Integer]
    case tokens of
        [] -> return ()
        (n:rest) -> do
            let vals = takeInteger (max 0 n) rest
            case vals of
                [] -> putStrLn "0"
                (x:xs) -> print (kadane xs x x)

takeInteger :: Integer -> [a] -> [a]
takeInteger n _ | n <= 0 = []
takeInteger _ [] = []
takeInteger n (x:xs) = x : takeInteger (n - 1) xs

kadane :: [Integer] -> Integer -> Integer -> Integer
kadane [] _ best = best
kadane (y:ys) cur best =
    let cur' = max y (cur + y)
        best' = max best cur'
    in kadane ys cur' best'