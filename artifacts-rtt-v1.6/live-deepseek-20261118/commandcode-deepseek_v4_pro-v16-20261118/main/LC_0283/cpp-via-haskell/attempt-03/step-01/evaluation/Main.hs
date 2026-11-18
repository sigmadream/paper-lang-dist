module Main where

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
        n = read (head tokens) :: Int
        nums = map read (take n (tail tokens)) :: [Int]
        (nonZeros, zeros) = foldr (\x (nz, zs) ->
                                    if x == 0 then (nz, x:zs)
                                              else (x:nz, zs))
                                  ([], []) nums
        result = nonZeros ++ zeros
    putStrLn $ unwords $ map show result