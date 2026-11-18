module Main where

solve :: Int -> [Integer] -> Integer
solve n xs
    | n <= 0 = 0
    | null xs = 0
    | otherwise =
        case xs of
            [a] -> a
            (a:b:rest) -> go rest 0 a (a + b) b
  where
    go [] _ _ dp1 _ = dp1
    go (score:rest) dp3 dp2 dp1 prev =
        let cur = max dp2 (dp3 + prev) + score
        in go rest dp2 dp1 cur score

main :: IO ()
main = do
    input <- getContents
    let vals = map read (words input) :: [Integer]
    case vals of
        [] -> return ()
        (n:rest) -> do
            let ni = fromIntegral n :: Int
                xs = take (max 0 ni) rest
            print (solve ni xs)