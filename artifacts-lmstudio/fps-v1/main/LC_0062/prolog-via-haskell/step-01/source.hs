import Control.Monad

main :: IO ()
main = do
    [m, n] <- map read . words <$> getLine
    let row = replicate n 1
        rows k r = if k == 0 then r else rows (k - 1) (zipWith (+) r (tail r))
        answer = last $ rows (m - 1) row
    print answer