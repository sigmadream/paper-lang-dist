import Data.Array

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (x:xs) ->
            let n = read x :: Int
                scores = map read (take n xs) :: [Int]
            in if n == 0
                then putStrLn "0"
                else do
                    let s = listArray (1, n) scores
                        dp = listArray (0, n) [value i | i <- [0..n]]
                        value 0 = 0
                        value 1 = s ! 1
                        value 2 = s ! 1 + s ! 2
                        value i = max (dp ! (i - 2)) (dp ! (i - 3) + s ! (i - 1)) + s ! i
                    print (dp ! n)