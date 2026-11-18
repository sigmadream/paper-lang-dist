import Data.Array
import qualified Data.Set as Set

mkPairs :: [Int] -> [(Int, Int)]
mkPairs (a:b:rest) = (a, b) : mkPairs rest
mkPairs _ = []

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Int]
    case nums of
        (n:m:rest) -> do
            let pairs = mkPairs (take (2 * m) rest)
                adj = accumArray (flip (:)) [] (1, n)
                        (concatMap (\(a, b) -> [(a, b), (b, a)]) pairs)
                neigh1 = adj ! 1
                set1 = Set.fromList neigh1
                set2 = Set.fromList (concatMap (\x -> adj ! x) neigh1)
                ans = Set.size (Set.delete 1 (Set.union set1 set2))
            print ans
        _ -> return ()