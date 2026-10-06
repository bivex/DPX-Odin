parser grammar OdinParser;

options {
    tokenVocab = OdinLexer;
}

compilationUnit
    : fileTag* packageDecl importDecl* topLevelDecl* EOF
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
    : constantDecl
    | variableDecl
    | foreignBlock
    | whenStmt
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
    : (USING | DIRECTIVE)? identList COLON type (STRING_LIT | RAW_STRING_LIT)?
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
    : BIT_SET LBRACK type (SEMI type)? RBRACK
    ;

procDecl
    : PROC callingConvention? LPAREN paramList? RPAREN (ARROW returnTypes)? procBody
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
    : (USING | DIRECTIVE)? identList COLON ELLIPSIS? type (EQUAL expr)?
    ;

returnTypes
    : LPAREN returnFieldList? RPAREN
    | type
    ;

returnFieldList
    : returnField (COMMA returnField)* COMMA?
    ;

returnField
    : (IDENT COLON)? type
    ;

procBody
    : block
    | MINUS MINUS MINUS SEMI?
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

returnStmt
    : RETURN exprList? SEMI?
    ;

deferStmt
    : DEFER stmt
    ;

ifStmt
    : IF (simpleStmt SEMI)? expr block (ELSE (ifStmt | block))?
    ;

whenStmt
    : WHEN expr block (ELSE (whenStmt | block))?
    ;

forStmt
    : FOR (forClause)? block
    ;

forClause
    : simpleStmt SEMI expr SEMI simpleStmt
    | IDENT (COMMA IDENT)? IN expr
    | expr
    ;

switchStmt
    : SWITCH (simpleStmt SEMI)? (expr | (IDENT IN expr))? LBRACE switchCase* RBRACE
    ;

switchCase
    : CASE exprList COLON stmt*
    | DEFAULT COLON stmt*
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
    : pointerType
    | sliceType
    | dynArrayType
    | arrayType
    | mapType
    | procType
    | distinctType
    | qualifiedIdent
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

procType
    : PROC callingConvention? LPAREN paramList? RPAREN (ARROW returnTypes)?
    ;

distinctType
    : DISTINCT type
    ;

qualifiedIdent
    : IDENT (DOT IDENT)*
    | CONTEXT (DOT IDENT)*
    | ANY
    ;

// Expressions
expr
    : expr QUESTION expr COLON expr                 # TernaryExpr
    | expr (PIPE_PIPE | OR_RETURN | OR_BREAK) expr  # LogicalOrExpr
    | expr AMP_AMP expr                            # LogicalAndExpr
    | expr (EQ | NEQ | LT | LE | GT | GE | INSTANCEOF) expr     # RelationalExpr
    | expr (PLUS | MINUS | PIPE | TILDE) expr       # AdditiveExpr
    | expr (STAR | SLASH | PERCENT | LT_LT | GT_GT | AMP) expr # MultiplicativeExpr
    | (PLUS | MINUS | EXCLAMATION | TILDE | CARET | AMP) expr  # UnaryExpr
    | (CAST | TRANSMUTE) LPAREN type RPAREN expr   # CastExpr
    | AUTO_CAST expr                               # AutoCastExpr
    | expr LPAREN argumentList? RPAREN             # CallExpr
    | expr LBRACK expr (ELLIPSIS expr?)? RBRACK    # IndexOrSliceExpr
    | expr DOT IDENT                               # MemberAccessExpr
    | expr CARET                                   # DerefExpr
    | literal                                      # LiteralExpr
    | qualifiedIdent                               # IdentifierExpr
    | compoundLiteral                              # CompoundLitExpr
    | LPAREN expr RPAREN                           # ParenExpr
    ;

argumentList
    : argument (COMMA argument)* COMMA?
    ;

argument
    : (IDENT EQUAL)? expr
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
