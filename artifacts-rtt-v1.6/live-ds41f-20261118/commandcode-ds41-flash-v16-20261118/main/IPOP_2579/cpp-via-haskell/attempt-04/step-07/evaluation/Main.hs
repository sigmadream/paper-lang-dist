module Main where

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Integer]
    case nums of
        [] -> return ()
        (n:rest) -> putStrLn (show (solve (fromIntegral n) rest))

solve :: Int -> [Integer] -> Integer
solve n xs
    | n <= 0 = 0
    | n == 1 = case xs of
        (a:_) -> a
        _ -> 0
    | n == 2 = case xs of
        (a:b:_) -> a + b
        _ -> 0
    | otherwise = case xs of
        (s1:s2:rest) ->
            let restN = take (n - 2) rest
            in go (s1 + s2) s1 0 s2 restN
        _ -> 0
  where
    go p1 _ _ _ [] = p1
    go p1 p2 p3 prev (cur:cs) =
        let nxt = max p2 (p3 + prev) + cur
        in go nxt p1 p2 cur cs