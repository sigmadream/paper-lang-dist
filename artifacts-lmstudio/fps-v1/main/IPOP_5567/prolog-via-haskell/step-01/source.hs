import Data.List (sort, nub, delete)

main :: IO ()
main = do
    [n, m] <- map read . words <$> getLine
    edges <- replicateM m $ do
        [a, b] <- map read . words <$> getLine
        return (a, b)
    let direct = [b | (1, b) <- edges]
    let second = nub [c | (a, c) <- edges, a `elem` direct]
    let allInvited = sort $ direct ++ second
    let invited = delete 1 allInvited
    print $ length invited