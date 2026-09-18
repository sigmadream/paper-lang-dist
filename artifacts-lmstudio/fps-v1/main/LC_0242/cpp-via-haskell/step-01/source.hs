import Data.List (all)

main :: IO ()
main = do
    s <- getLine
    t <- getLine
    let counts = [sum $ map ((==) i . snd) [(i, count c t) | c <- ['a'..'z']]) | i <- ['a'..'z']]
    print $ if all (== 0) counts then 1 else 0

count :: Char -> String -> Int
count c = length . filter (== c)