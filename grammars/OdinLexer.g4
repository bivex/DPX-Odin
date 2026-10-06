lexer grammar OdinLexer;

// Keywords
PACKAGE     : 'package';
IMPORT      : 'import';
FOREIGN     : 'foreign';
STRUCT      : 'struct';
UNION       : 'union';
ENUM        : 'enum';
BIT_SET     : 'bit_set';
MAP         : 'map';
DYNAMIC     : 'dynamic';
PROC        : 'proc';
RETURN      : 'return';
DEFER       : 'defer';
IF          : 'if';
ELSE        : 'else';
WHEN        : 'when';
FOR         : 'for';
IN          : 'in';
SWITCH      : 'switch';
CASE        : 'case';
DEFAULT     : 'default';
CAST        : 'cast';
AUTO_CAST   : 'auto_cast';
TRANSMUTE   : 'transmute';
USING       : 'using';
OR_RETURN   : 'or_return';
OR_BREAK    : 'or_break';
OR_CONTINUE : 'or_continue';
BREAK       : 'break';
CONTINUE    : 'continue';
FALLTHROUGH : 'fallthrough';
CONTEXT     : 'context';
DISTINCT    : 'distinct';
TYPEID      : 'typeid';
RAWPTR      : 'rawptr';
ANY         : 'any';
NIL         : 'nil';
INSTANCEOF  : 'instanceof';

// Directives and Attributes
FILE_TAG    : '#+' [a-zA-Z_] [a-zA-Z0-9_]* ~[\r\n]*;
DIRECTIVE   : '#' [a-zA-Z_] [a-zA-Z0-9_]*;
ATTRIBUTE   : '@' ( '(' (~[)\r\n])* ')' | [a-zA-Z_] [a-zA-Z0-9_]* );

// Operators and Punctuation
COLON_COLON : '::';
COLON_EQUAL : ':=';
ARROW       : '->';
ELLIPSIS    : '..';
DOT         : '.';
COMMA       : ',';
SEMI        : ';';
COLON       : ':';
QUESTION    : '?';
CARET       : '^';
DOLLAR      : '$';
LPAREN      : '(';
RPAREN      : ')';
LBRACK      : '[';
RBRACK      : ']';
LBRACE      : '{';
RBRACE      : '}';
EQUAL       : '=';
PLUS_EQUAL  : '+=';
MINUS_EQUAL : '-=';
STAR_EQUAL  : '*=';
SLASH_EQUAL : '/=';
PLUS        : '+';
MINUS       : '-';
STAR        : '*';
SLASH       : '/';
PERCENT     : '%';
AMP_AMP     : '&&';
PIPE_PIPE   : '||';
AMP         : '&';
PIPE        : '|';
TILDE       : '~';
EXCLAMATION : '!';
LT_LT       : '<<';
GT_GT       : '>>';
LE          : '<=';
GE          : '>=';
EQ          : '==';
NEQ         : '!=';
LT          : '<';
GT          : '>';

// Literals
FLOAT_LIT
    : [0-9]+ '.' [0-9]+ ([eE] [+-]? [0-9]+)?
    | [0-9]+ [eE] [+-]? [0-9]+
    ;

HEX_LIT
    : '0' [xX] [0-9a-fA-F_]+
    ;

BIN_LIT
    : '0' [bB] [01_]+
    ;

OCT_LIT
    : '0' [oO] [0-7_]+
    ;

INT_LIT
    : [0-9] [0-9_]*
    ;

STRING_LIT
    : '"' (~["\\\r\n] | '\\' .)* '"'
    ;

RAW_STRING_LIT
    : '`' ~[`]* '`'
    ;

RUNE_LIT
    : '\'' (~['\\\r\n] | '\\' .)* '\''
    ;

// Identifiers
IDENT
    : [a-zA-Z_] [a-zA-Z0-9_]*
    ;

// Comments and Whitespace
LINE_COMMENT
    : '//' ~[\r\n]* -> channel(HIDDEN)
    ;

BLOCK_COMMENT
    : '/*' .*? '*/' -> channel(HIDDEN)
    ;

SHEBANG
    : '#!' ~[\r\n]* -> channel(HIDDEN)
    ;

WS
    : [ \t\r\n]+ -> skip
    ;
