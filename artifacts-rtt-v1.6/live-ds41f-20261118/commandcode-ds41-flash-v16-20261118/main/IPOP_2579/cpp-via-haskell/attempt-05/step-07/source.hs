module Main where

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (nStr:rest) -> do
            let n = read nStr :: Int
                scores = map read (take n rest) :: [Int]
            print (solve scores)

solve :: [Int] -> Int
solve [] = 0
solve [a] = a
solve (a:b:rest) =
    let negInf = -1000000000
        prev2 = (a, negInf)
        curr = (a + b, b)
    in go curr prev2 rest
  where
    go (one, two) _ [] = max one two
    go (oPrev, tPrev) (oPrev2, tPrev2) (x:xs) =
        let one = tPrev + x
            two = max oPrev2 tPrev2 + x
        in go (one, two) (oPrev, tPrev) xs