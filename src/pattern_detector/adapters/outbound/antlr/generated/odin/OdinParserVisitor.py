# Generated from grammars/OdinParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .OdinParser import OdinParser
else:
    from OdinParser import OdinParser

# This class defines a complete generic visitor for a parse tree produced by OdinParser.

class OdinParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by OdinParser#compilationUnit.
    def visitCompilationUnit(self, ctx:OdinParser.CompilationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#fileTag.
    def visitFileTag(self, ctx:OdinParser.FileTagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#packageDecl.
    def visitPackageDecl(self, ctx:OdinParser.PackageDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#importDecl.
    def visitImportDecl(self, ctx:OdinParser.ImportDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#foreignImportBlock.
    def visitForeignImportBlock(self, ctx:OdinParser.ForeignImportBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#topLevelDecl.
    def visitTopLevelDecl(self, ctx:OdinParser.TopLevelDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#foreignBlock.
    def visitForeignBlock(self, ctx:OdinParser.ForeignBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#constantDecl.
    def visitConstantDecl(self, ctx:OdinParser.ConstantDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#variableDecl.
    def visitVariableDecl(self, ctx:OdinParser.VariableDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#identList.
    def visitIdentList(self, ctx:OdinParser.IdentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#exprList.
    def visitExprList(self, ctx:OdinParser.ExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#typeList.
    def visitTypeList(self, ctx:OdinParser.TypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#typeOrExpr.
    def visitTypeOrExpr(self, ctx:OdinParser.TypeOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#structDecl.
    def visitStructDecl(self, ctx:OdinParser.StructDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#structFieldList.
    def visitStructFieldList(self, ctx:OdinParser.StructFieldListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#structField.
    def visitStructField(self, ctx:OdinParser.StructFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#unionDecl.
    def visitUnionDecl(self, ctx:OdinParser.UnionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#enumDecl.
    def visitEnumDecl(self, ctx:OdinParser.EnumDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#enumMemberList.
    def visitEnumMemberList(self, ctx:OdinParser.EnumMemberListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#enumMember.
    def visitEnumMember(self, ctx:OdinParser.EnumMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#bitSetDecl.
    def visitBitSetDecl(self, ctx:OdinParser.BitSetDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#procDecl.
    def visitProcDecl(self, ctx:OdinParser.ProcDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#procGroup.
    def visitProcGroup(self, ctx:OdinParser.ProcGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#callingConvention.
    def visitCallingConvention(self, ctx:OdinParser.CallingConventionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#polyParams.
    def visitPolyParams(self, ctx:OdinParser.PolyParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#polyParamList.
    def visitPolyParamList(self, ctx:OdinParser.PolyParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#polyParam.
    def visitPolyParam(self, ctx:OdinParser.PolyParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#paramList.
    def visitParamList(self, ctx:OdinParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#param.
    def visitParam(self, ctx:OdinParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#returnTypes.
    def visitReturnTypes(self, ctx:OdinParser.ReturnTypesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#returnFieldList.
    def visitReturnFieldList(self, ctx:OdinParser.ReturnFieldListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#returnField.
    def visitReturnField(self, ctx:OdinParser.ReturnFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#procBody.
    def visitProcBody(self, ctx:OdinParser.ProcBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#block.
    def visitBlock(self, ctx:OdinParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#stmt.
    def visitStmt(self, ctx:OdinParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#returnStmt.
    def visitReturnStmt(self, ctx:OdinParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#deferStmt.
    def visitDeferStmt(self, ctx:OdinParser.DeferStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#ifStmt.
    def visitIfStmt(self, ctx:OdinParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#whenStmt.
    def visitWhenStmt(self, ctx:OdinParser.WhenStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#forStmt.
    def visitForStmt(self, ctx:OdinParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#forClause.
    def visitForClause(self, ctx:OdinParser.ForClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#switchStmt.
    def visitSwitchStmt(self, ctx:OdinParser.SwitchStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#switchCase.
    def visitSwitchCase(self, ctx:OdinParser.SwitchCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#assignStmt.
    def visitAssignStmt(self, ctx:OdinParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#assignOp.
    def visitAssignOp(self, ctx:OdinParser.AssignOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#simpleStmt.
    def visitSimpleStmt(self, ctx:OdinParser.SimpleStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#exprStmt.
    def visitExprStmt(self, ctx:OdinParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#type.
    def visitType(self, ctx:OdinParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#pointerType.
    def visitPointerType(self, ctx:OdinParser.PointerTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#sliceType.
    def visitSliceType(self, ctx:OdinParser.SliceTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#dynArrayType.
    def visitDynArrayType(self, ctx:OdinParser.DynArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#arrayType.
    def visitArrayType(self, ctx:OdinParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#mapType.
    def visitMapType(self, ctx:OdinParser.MapTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#procType.
    def visitProcType(self, ctx:OdinParser.ProcTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#distinctType.
    def visitDistinctType(self, ctx:OdinParser.DistinctTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#qualifiedIdent.
    def visitQualifiedIdent(self, ctx:OdinParser.QualifiedIdentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#AutoCastExpr.
    def visitAutoCastExpr(self, ctx:OdinParser.AutoCastExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#DerefExpr.
    def visitDerefExpr(self, ctx:OdinParser.DerefExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#RelationalExpr.
    def visitRelationalExpr(self, ctx:OdinParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#IndexOrSliceExpr.
    def visitIndexOrSliceExpr(self, ctx:OdinParser.IndexOrSliceExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#UnaryExpr.
    def visitUnaryExpr(self, ctx:OdinParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#LogicalAndExpr.
    def visitLogicalAndExpr(self, ctx:OdinParser.LogicalAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#LogicalOrExpr.
    def visitLogicalOrExpr(self, ctx:OdinParser.LogicalOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#MultiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:OdinParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#AdditiveExpr.
    def visitAdditiveExpr(self, ctx:OdinParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#IdentifierExpr.
    def visitIdentifierExpr(self, ctx:OdinParser.IdentifierExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#CastExpr.
    def visitCastExpr(self, ctx:OdinParser.CastExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#LiteralExpr.
    def visitLiteralExpr(self, ctx:OdinParser.LiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#CompoundLitExpr.
    def visitCompoundLitExpr(self, ctx:OdinParser.CompoundLitExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#CallExpr.
    def visitCallExpr(self, ctx:OdinParser.CallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#ParenExpr.
    def visitParenExpr(self, ctx:OdinParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#MemberAccessExpr.
    def visitMemberAccessExpr(self, ctx:OdinParser.MemberAccessExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#TernaryExpr.
    def visitTernaryExpr(self, ctx:OdinParser.TernaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#argumentList.
    def visitArgumentList(self, ctx:OdinParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#argument.
    def visitArgument(self, ctx:OdinParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#compoundLiteral.
    def visitCompoundLiteral(self, ctx:OdinParser.CompoundLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OdinParser#literal.
    def visitLiteral(self, ctx:OdinParser.LiteralContext):
        return self.visitChildren(ctx)



del OdinParser