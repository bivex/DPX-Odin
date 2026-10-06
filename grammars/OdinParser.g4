parser grammar OdinParser;

options {
    tokenVocab = OdinLexer;
}

compilationUnit
    : fileTag* packageDecl? topLevelDecl* EOF
    ;

fileTag
    : FILE_TAG SEMI?
    ;

packageDecl
    : PACKAGE qualifiedIdent SEMI?
    ;

importDecl
    : ATTRIBUTE* IMPORT IDENT? (STRING_LIT | RAW_STRING_LIT) SEMI?
    | ATTRIBUTE* FOREIGN IMPORT IDENT? (STRING_LIT | RAW_STRING_LIT | foreignImportBlock) SEMI?
    ;

foreignImportBlock
    : LBRACE (STRING_LIT | RAW_STRING_LIT | COMMA)* RBRACE
    ;

topLevelDecl
    : importDecl
    | constantDecl
    | variableDecl
    | foreignBlock
    | whenStmt
    | directiveStmt
    | SEMI
    ;

foreignBlock
    : ATTRIBUTE* FOREIGN IDENT? LBRACE topLevelDecl* RBRACE SEMI?
    ;

constantDecl
    : ATTRIBUTE* IDENT COLON_COLON typeOrExpr SEMI?
    | ATTRIBUTE* IDENT COLON type COLON expr SEMI?
    ;

variableDecl
    : ATTRIBUTE* identList COLON_EQUAL exprList SEMI?
    | ATTRIBUTE* identList COLON type (EQUAL exprList)? SEMI?
    ;

identList
    : IDENT (COMMA IDENT)*
    ;

exprList
    : expr (COMMA expr)* COMMA?
    ;

typeList
    : type (COMMA type)* COMMA?
    ;

typeOrExpr
    : structDecl
    | unionDecl
    | enumDecl
    | bitSetDecl
    | procDecl
    | procGroup
    | type
    | expr
    ;

structDecl
    : STRUCT polyParams? DIRECTIVE* LBRACE structFieldList? RBRACE
    ;

structFieldList
    : structField ( (SEMI | COMMA) structField )* (SEMI | COMMA)?
    ;

structField
    : (USING | DIRECTIVE)? identList (COLON ELLIPSIS? type (EQUAL expr)? (STRING_LIT | RAW_STRING_LIT)? | COLON_EQUAL expr)
    | (USING | DIRECTIVE)? type (STRING_LIT | RAW_STRING_LIT)?
    ;

unionDecl
    : UNION polyParams? DIRECTIVE* LBRACE typeList? RBRACE
    ;

enumDecl
    : ENUM type? LBRACE enumMemberList? RBRACE
    ;

enumMemberList
    : enumMember ( (SEMI | COMMA) enumMember )* (SEMI | COMMA)?
    ;

enumMember
    : IDENT (EQUAL expr)?
    ;

bitSetDecl
    : BIT_SET LBRACK (type | expr) (SEMI (type | expr))? RBRACK
    ;

procDecl
    : PROC callingConvention? LPAREN paramList? RPAREN (ARROW returnTypes)? DIRECTIVE* (WHERE exprList)? DIRECTIVE* procBody
    ;

procGroup
    : PROC LBRACE exprList? RBRACE
    ;

callingConvention
    : STRING_LIT
    ;

polyParams
    : LPAREN polyParamList? RPAREN
    ;

polyParamList
    : polyParam (COMMA polyParam)* COMMA?
    ;

polyParam
    : DOLLAR? IDENT COLON (TYPEID | type)
    ;

paramList
    : param (COMMA param)* COMMA?
    ;

param
    : (USING | DIRECTIVE)? (identList | DOLLAR IDENT) COLON ELLIPSIS? type (EQUAL expr)?
    | (USING | DIRECTIVE)? identList COLON_EQUAL expr
    | ELLIPSIS? type
    ;

returnTypes
    : LPAREN returnFieldList? RPAREN
    | type
    ;

returnFieldList
    : returnField (COMMA returnField)* COMMA?
    ;

returnField
    : (IDENT COLON)? (type | EXCLAMATION)
    ;

procBody
    : block
    | MINUS MINUS MINUS SEMI?
    | DO stmt
    ;

block
    : LBRACE stmt* RBRACE
    ;

stmt
    : returnStmt
    | deferStmt
    | ifStmt
    | whenStmt
    | forStmt
    | switchStmt
    | labelStmt
    | directiveStmt
    | variableDecl
    | constantDecl
    | assignStmt
    | exprStmt
    | block
    | BREAK IDENT? SEMI?
    | CONTINUE IDENT? SEMI?
    | FALLTHROUGH SEMI?
    | SEMI
    ;

labelStmt
    : IDENT COLON (forStmt | switchStmt | block)
    ;

directiveStmt
    : DIRECTIVE (LPAREN argumentList? RPAREN)? SEMI?
    ;

returnStmt
    : RETURN exprList? SEMI?
    ;

deferStmt
    : DEFER stmt
    ;

ifStmt
    : IF (simpleStmt SEMI)? expr (block | DO stmt) (ELSE (ifStmt | block | DO stmt))?
    ;

whenStmt
    : WHEN expr (block | DO stmt) (ELSE (whenStmt | block | DO stmt))?
    ;

forStmt
    : FOR (forClause)? (block | DO stmt)
    ;

forClause
    : simpleStmt SEMI expr SEMI simpleStmt
    | (identList)? (IN | NOT_IN) expr
    | expr
    ;

switchStmt
    : DIRECTIVE* SWITCH (simpleStmt SEMI)? (expr | ((identList)? (IN | NOT_IN) expr))? LBRACE switchCase* RBRACE
    ;

switchCase
    : CASE (exprList | typeList)? (COLON | DO) stmt*
    | DEFAULT (COLON | DO)? stmt*
    ;

assignStmt
    : exprList assignOp exprList SEMI?
    ;

assignOp
    : EQUAL
    | PLUS_EQUAL
    | MINUS_EQUAL
    | STAR_EQUAL
    | SLASH_EQUAL
    ;

simpleStmt
    : variableDecl
    | assignStmt
    | expr
    ;

exprStmt
    : expr SEMI?
    ;

// Types
type
    : DIRECTIVE* pointerType
    | DIRECTIVE* sliceType
    | DIRECTIVE* dynArrayType
    | DIRECTIVE* arrayType
    | DIRECTIVE* mapType
    | DIRECTIVE* matrixType
    | DIRECTIVE* procType
    | DIRECTIVE* structDecl
    | DIRECTIVE* unionDecl
    | DIRECTIVE* enumDecl
    | DIRECTIVE* bitSetDecl
    | DIRECTIVE* distinctType
    | DIRECTIVE* polyType
    | DIRECTIVE* specializedType
    | DIRECTIVE* qualifiedIdent
    ;

pointerType
    : CARET type
    | LBRACK CARET RBRACK type
    | RAWPTR
    ;

sliceType
    : LBRACK RBRACK type
    ;

dynArrayType
    : LBRACK DYNAMIC (SEMI expr)? RBRACK type
    ;

arrayType
    : LBRACK (expr | QUESTION) RBRACK type
    ;

mapType
    : MAP LBRACK type RBRACK type
    ;

matrixType
    : MATRIX LBRACK expr COMMA expr RBRACK type
    ;

procType
    : PROC callingConvention? LPAREN paramList? RPAREN (ARROW returnTypes)? DIRECTIVE*
    ;

distinctType
    : DISTINCT type
    ;

polyType
    : DOLLAR IDENT
    ;

specializedType
    : qualifiedIdent LPAREN (typeList | exprList)? RPAREN
    ;

qualifiedIdent
    : IDENT (DOT IDENT)*
    | CONTEXT (DOT IDENT)*
    | ANY
    ;

// Expressions
expr
    : expr QUESTION expr COLON expr                               # TernaryExpr
    | expr (OR_RETURN | OR_BREAK | OR_CONTINUE)                   # PostfixControlExpr
    | expr PIPE_PIPE expr                                         # LogicalOrExpr
    | expr AMP_AMP expr                                           # LogicalAndExpr
    | expr (EQ | NEQ | LT | LE | GT | GE | INSTANCEOF) expr       # RelationalExpr
    | expr (IN | NOT_IN) expr                                     # InExpr
    | expr (RANGE_HALF_OPEN | RANGE_CLOSED | ELLIPSIS) expr       # RangeExpr
    | expr (PLUS | MINUS | PIPE | TILDE) expr                     # AdditiveExpr
    | expr (STAR | SLASH | PERCENT | LT_LT | GT_GT | AMP) expr    # MultiplicativeExpr
    | (PLUS | MINUS | EXCLAMATION | TILDE | CARET | AMP) expr     # UnaryExpr
    | (CAST | TRANSMUTE) LPAREN type RPAREN expr                  # CastExpr
    | AUTO_CAST expr                                              # AutoCastExpr
    | expr LPAREN argumentList? RPAREN                            # CallExpr
    | expr LBRACK (expr | ELLIPSIS)? ((ELLIPSIS | RANGE_HALF_OPEN | RANGE_CLOSED | COLON) expr?)? (COMMA expr)* RBRACK # IndexOrSliceExpr
    | expr DOT IDENT                                              # MemberAccessExpr
    | expr DOT LPAREN type RPAREN                                 # TypeAssertExpr
    | expr CARET                                                  # DerefExpr
    | DOT IDENT                                                   # ImplicitSelectorExpr
    | DIRECTIVE (LPAREN argumentList? RPAREN)?                    # DirectiveExpr
    | literal                                                     # LiteralExpr
    | TYPEID                                                      # TypeidExpr
    | DOLLAR IDENT                                                # PolyParamExpr
    | qualifiedIdent                                              # IdentifierExpr
    | compoundLiteral                                             # CompoundLitExpr
    | LPAREN expr RPAREN                                          # ParenExpr
    ;

argumentList
    : argument (COMMA argument)* COMMA?
    ;

argument
    : (IDENT EQUAL)? (type | expr)
    | DOT IDENT EQUAL (type | expr)
    ;

compoundLiteral
    : type? LBRACE argumentList? RBRACE
    ;

literal
    : INT_LIT
    | FLOAT_LIT
    | HEX_LIT
    | BIN_LIT
    | OCT_LIT
    | STRING_LIT
    | RAW_STRING_LIT
    | RUNE_LIT
    | NIL
    ;
