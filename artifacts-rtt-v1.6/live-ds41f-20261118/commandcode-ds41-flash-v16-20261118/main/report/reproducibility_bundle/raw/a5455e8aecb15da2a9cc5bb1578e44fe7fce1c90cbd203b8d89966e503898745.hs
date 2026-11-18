import Data.List (nub)

toPairs :: [Int] -> [(Int, Int)]
toPairs (a:b:rest) = (a, b) : toPairs rest
toPairs _ = []

main :: IO ()
main = do
    input <- getContents
    let xs = map read (words input) :: [Int]
    case xs of
        (n:m:rest) -> do
            let edges = toPairs (take (2 * m) rest)
                direct = nub [if a == 1 then b else a | (a, b) <- edges, a == 1 || b == 1]
                cand = [b | (a, b) <- edges, a `elem` direct]
                    ++ [a | (a, b) <- edges, b `elem` direct]
                distance2 = nub [v | v <- cand, v /= 1, v `notElem` direct]
                answer = length direct + length distance2
            print answer
        _ -> return ()