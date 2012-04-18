{-# LANGUAGE OverlappingInstances #-}
{-# LANGUAGE FlexibleInstances #-}
import System.IO
import System.Environment
import Text.Parsec hiding(label)
import Text.Parsec.String

type Program = [Block]
data Block = Block {
    label :: Maybe String
    , statements :: [String]
    } deriving (Show)

class Pretty a where
    prettyPrint :: a -> String

instance Pretty (Block) where 
    prettyPrint (Block (Just a) sts) = a ++ ":\n" ++ prettyPrint sts
    prettyPrint (Block (Nothing) sts) = prettyPrint sts

instance Pretty String where 
    prettyPrint s = "\t"++s

instance Pretty a => Pretty [a] where 
    prettyPrint [] = ""
    prettyPrint (x:xs) = prettyPrint x ++ "\n" ++ prettyPrint xs

fmap' :: ([String] -> [String]) -> Program -> Program
fmap' f p = map (g f) p
        where g f (Block l s) =  Block l (f s)

parseLabel :: Parser String
parseLabel = do 
    many space 
    first <- many1 alphaNum
    char  ':'
    many space 
    return first

parseStatement :: Parser String 
parseStatement = do 
    skipMany space
    w <- many1 (noneOf ['\n',':'])
    (newline) <|> (eof >> return ' ')
    return w

parseBlock :: Parser Block 
parseBlock = do 
    x <- optionMaybe (try parseLabel)
    y <- many1 (try parseStatement)
    return (Block x y)
parseProgram :: Parser Program
parseProgram = do 
    x <-  many1 (try parseBlock)
    return x

statement_li :: Parser (String,Int)
statement_li  = do 
    string "li"
    skipMany space 
    r <- char '$' >>  many1 alphaNum
    skipMany space 
    optional (char ',')
    skipMany space 
    num <- many1 digit
    skipMany space 
    return ("$"++r,read num)

statement_sub :: Parser (String,String,String)
statement_sub = do 
    string "sub"
    skipMany space 
    r1 <- char '$' >>  many1 alphaNum
    skipMany space 
    optional (char ',')
    skipMany space 
    r2 <- char '$' >>  many1 alphaNum
    skipMany space 
    optional (char ',')
    skipMany space 
    r3 <- char '$' >>  many1 alphaNum
    skipMany space 
    return ("$"++r1,"$"++r2,"$"++r3)

statement_move :: Parser (String,String)
statement_move  = do 
    string "move"
    skipMany space 
    r <- char '$' >>  many1 alphaNum
    skipMany space 
    optional (char ',')
    skipMany space 
    s <- char '$' >> many1 alphaNum
    skipMany space 
    return ("$"++r,"$"++s)

statement_lw :: Parser (String,String)
statement_lw  = do 
    try (string  "lw") <|> string "l.s"
    skipMany space 
    r <- char '$' >>  many1 alphaNum
    skipMany space 
    optional (char ',')
    skipMany space 
    s <- many1 (alphaNum <|> char '$' <|> char '(' <|> char ')' <|> char '-')
    skipMany space 
    return ("$"++r,s)

statement_sw :: Parser (String,String)
statement_sw  = do 
    try (string "sw") <|> string "s.s"
    skipMany space 
    r <- char '$' >>  many1 alphaNum
    skipMany space 
    optional (char ',')
    skipMany space 
    s <- many1 (alphaNum <|> char '$' <|> char '(' <|> char ')' <|> char '-')
    skipMany space 
    return ("$"++r,s)

remove_reloading [] = []
remove_reloading [x] = [x]
remove_reloading (x:y:ys) = case parse statement_sw "" x of 
                                Left err -> x:remove_reloading (y:ys)
                                Right (r1,s1) -> case parse statement_lw "" y of 
                                    Left err -> x:remove_reloading (y:ys)
                                    Right (r2,s2) -> if r1==r2 && s1==s2 
                                        then x:remove_reloading ys
                                        else x:y:remove_reloading ys










stackSub [] m = ([],0) 
stackSub [x] m = ([x],0)
stackSub (x:y:xs) m = case parse (try statement_move <|> statement_lw)  "" x of 
        Left err -> ps x y xs m
        Right (r1,r2) -> if r1=="$sp" || r2=="$sp" 
                            then let (res,v) = ps x y xs True
                                    in (res,0)
                            else ps x y xs m
    where ps x y xs m = case parse statement_li "" x  of 
                        Left err -> do let (rest,v) = stackSub (y:xs) m
                                       (x:rest,v)
                        Right (r,v) -> case  parse statement_sub "" y of 
                                            Left err -> do let (rest,v) = stackSub (y:xs) m
                                                           (x:rest,v)
                                            Right (r1,r2,r3) -> if (r1=="$sp") && (r2=="$sp") && (r==r3)
                                                                    then if m 
                                                                        then do 
                                                                            let (rest,val) = stackSub xs False
                                                                            (("li "++r++" "++show(v+val)):y:rest,v+val)
                                                                        else do 
                                                                            let (rest,val) = stackSub xs m
                                                                            (rest,val+v)
                                                                    else 
                                                                        let (rest,val) = stackSub (y:xs) m
                                                                            in (x:rest,val)


main = do 
    (x:_) <- getArgs
    c <- readFile x
    case parse parseProgram "" c  of
        Left err -> print "Error while parsing" >> print err 
        Right val -> putStrLn $ prettyPrint (fmap' (\a -> remove_reloading (fst $ stackSub a True)) val)
