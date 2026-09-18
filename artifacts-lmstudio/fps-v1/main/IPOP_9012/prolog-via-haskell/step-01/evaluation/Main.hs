import Text.Read (readMaybe)
import Data.List (intercalate)

isBalanced :: String -> Bool
isBalanced = go 0 where
    go d [] = d == 0
    go d ('(' : xs) = go (d + 1) xs
    go d (')' : xs) | d > 0     = go (d - 1) xs
                    | otherwise = False

main :: IO ()
main = do
    t <- readLn :: IO Int
    inputs <- replicateM t getLine
    mapM_ (\s -> if isBalanced s then putStrLn "YES" else putStrLn "NO") inputs