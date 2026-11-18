module Main where

solve :: Int -> [Int] -> Int
solve n xs
    | n <= 0 = 0
    | n == 1 = case xs of
        (x:_) -> x
        []    -> 0
    | n == 2 = case xs of
        (x:y:_) -> x + y
        _       -> 0
    | length xs < 2 = 0
    | otherwise =
        let (s1:s2:rest) = xs
            limit = min (length xs) n
            (p1, _, _, _) = foldl step (s1 + s2, s1, 0, s2) (take (limit - 2) rest)
            step (p1, p2, p3, prev) cur =
                let nxt = max p2 (p3 + prev) + cur
                in (nxt, p1, p2, cur)
        in p1

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Int]
    case nums of
        [] -> return ()
        (n:xs) -> print (solve n xs)