# Generated from grammars/OdinParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .OdinParser import OdinParser
else:
    from OdinParser import OdinParser

# This class defines a complete listener for a parse tree produced by OdinParser.
class OdinParserListener(ParseTreeListener):

    # Enter a parse tree produced by OdinParser#compilationUnit.
    def enterCompilationUnit(self, ctx:OdinParser.CompilationUnitContext):
        pass

    # Exit a parse tree produced by OdinParser#compilationUnit.
    def exitCompilationUnit(self, ctx:OdinParser.CompilationUnitContext):
        pass


    # Enter a parse tree produced by OdinParser#fileTag.
    def enterFileTag(self, ctx:OdinParser.FileTagContext):
        pass

    # Exit a parse tree produced by OdinParser#fileTag.
    def exitFileTag(self, ctx:OdinParser.FileTagContext):
        pass


    # Enter a parse tree produced by OdinParser#packageDecl.
    def enterPackageDecl(self, ctx:OdinParser.PackageDeclContext):
        pass

    # Exit a parse tree produced by OdinParser#packageDecl.
    def exitPackageDecl(self, ctx:OdinParser.PackageDeclContext):
        pass


    # Enter a parse tree produced by OdinParser#importDecl.
    def enterImportDecl(self, ctx:OdinParser.ImportDeclContext):
        pass

    # Exit a parse tree produced by OdinParser#importDecl.
    def exitImportDecl(self, ctx:OdinParser.ImportDeclContext):
        pass


    # Enter a parse tree produced by OdinParser#foreignImportBlock.
    def enterForeignImportBlock(self, ctx:OdinParser.ForeignImportBlockContext):
        pass

    # Exit a parse tree produced by OdinParser#foreignImportBlock.
    def exitForeignImportBlock(self, ctx:OdinParser.ForeignImportBlockContext):
        pass


    # Enter a parse tree produced by OdinParser#topLevelDecl.
    def enterTopLevelDecl(self, ctx:OdinParser.TopLevelDeclContext):
        pass

    # Exit a parse tree produced by OdinParser#topLevelDecl.
    def exitTopLevelDecl(self, ctx:OdinParser.TopLevelDeclContext):
        pass


    # Enter a parse tree produced by OdinParser#foreignBlock.
    def enterForeignBlock(self, ctx:OdinParser.ForeignBlockContext):
        pass

    # Exit a parse tree produced by OdinParser#foreignBlock.
    def exitForeignBlock(self, ctx:OdinParser.ForeignBlockContext):
        pass


    # Enter a parse tree produced by OdinParser#constantDecl.
    def enterConstantDecl(self, ctx:OdinParser.ConstantDeclContext):
        pass

    # Exit a parse tree produced by OdinParser#constantDecl.
    def exitConstantDecl(self, ctx:OdinParser.ConstantDeclContext):
        pass


    # Enter a parse tree produced by OdinParser#variableDecl.
    def enterVariableDecl(self, ctx:OdinParser.VariableDeclContext):
        pass

    # Exit a parse tree produced by OdinParser#variableDecl.
    def exitVariableDecl(self, ctx:OdinParser.VariableDeclContext):
        pass


    # Enter a parse tree produced by OdinParser#identList.
    def enterIdentList(self, ctx:OdinParser.IdentListContext):
        pass

    # Exit a parse tree produced by OdinParser#identList.
    def exitIdentList(self, ctx:OdinParser.IdentListContext):
        pass


    # Enter a parse tree produced by OdinParser#exprList.
    def enterExprList(self, ctx:OdinParser.ExprListContext):
        pass

    # Exit a parse tree produced by OdinParser#exprList.
    def exitExprList(self, ctx:OdinParser.ExprListContext):
        pass


    # Enter a parse tree produced by OdinParser#typeList.
    def enterTypeList(self, ctx:OdinParser.TypeListContext):
        pass

    # Exit a parse tree produced by OdinParser#typeList.
    def exitTypeList(self, ctx:OdinParser.TypeListContext):
        pass


    # Enter a parse tree produced by OdinParser#typeOrExpr.
    def enterTypeOrExpr(self, ctx:OdinParser.TypeOrExprContext):
        pass

    # Exit a parse tree produced by OdinParser#typeOrExpr.
    def exitTypeOrExpr(self, ctx:OdinParser.TypeOrExprContext):
        pass


    # Enter a parse tree produced by OdinParser#structDecl.
    def enterStructDecl(self, ctx:OdinParser.StructDeclContext):
        pass

    # Exit a parse tree produced by OdinParser#structDecl.
    def exitStructDecl(self, ctx:OdinParser.StructDeclContext):
        pass


    # Enter a parse tree produced by OdinParser#structFieldList.
    def enterStructFieldList(self, ctx:OdinParser.StructFieldListContext):
        pass

    # Exit a parse tree produced by OdinParser#structFieldList.
    def exitStructFieldList(self, ctx:OdinParser.StructFieldListContext):
        pass


    # Enter a parse tree produced by OdinParser#structField.
    def enterStructField(self, ctx:OdinParser.StructFieldContext):
        pass

    # Exit a parse tree produced by OdinParser#structField.
    def exitStructField(self, ctx:OdinParser.StructFieldContext):
        pass


    # Enter a parse tree produced by OdinParser#unionDecl.
    def enterUnionDecl(self, ctx:OdinParser.UnionDeclContext):
        pass

    # Exit a parse tree produced by OdinParser#unionDecl.
    def exitUnionDecl(self, ctx:OdinParser.UnionDeclContext):
        pass


    # Enter a parse tree produced by OdinParser#enumDecl.
    def enterEnumDecl(self, ctx:OdinParser.EnumDeclContext):
        pass

    # Exit a parse tree produced by OdinParser#enumDecl.
    def exitEnumDecl(self, ctx:OdinParser.EnumDeclContext):
        pass


    # Enter a parse tree produced by OdinParser#enumMemberList.
    def enterEnumMemberList(self, ctx:OdinParser.EnumMemberListContext):
        pass

    # Exit a parse tree produced by OdinParser#enumMemberList.
    def exitEnumMemberList(self, ctx:OdinParser.EnumMemberListContext):
        pass


    # Enter a parse tree produced by OdinParser#enumMember.
    def enterEnumMember(self, ctx:OdinParser.EnumMemberContext):
        pass

    # Exit a parse tree produced by OdinParser#enumMember.
    def exitEnumMember(self, ctx:OdinParser.EnumMemberContext):
        pass


    # Enter a parse tree produced by OdinParser#bitSetDecl.
    def enterBitSetDecl(self, ctx:OdinParser.BitSetDeclContext):
        pass

    # Exit a parse tree produced by OdinParser#bitSetDecl.
    def exitBitSetDecl(self, ctx:OdinParser.BitSetDeclContext):
        pass


    # Enter a parse tree produced by OdinParser#procDecl.
    def enterProcDecl(self, ctx:OdinParser.ProcDeclContext):
        pass

    # Exit a parse tree produced by OdinParser#procDecl.
    def exitProcDecl(self, ctx:OdinParser.ProcDeclContext):
        pass


    # Enter a parse tree produced by OdinParser#procGroup.
    def enterProcGroup(self, ctx:OdinParser.ProcGroupContext):
        pass

    # Exit a parse tree produced by OdinParser#procGroup.
    def exitProcGroup(self, ctx:OdinParser.ProcGroupContext):
        pass


    # Enter a parse tree produced by OdinParser#callingConvention.
    def enterCallingConvention(self, ctx:OdinParser.CallingConventionContext):
        pass

    # Exit a parse tree produced by OdinParser#callingConvention.
    def exitCallingConvention(self, ctx:OdinParser.CallingConventionContext):
        pass


    # Enter a parse tree produced by OdinParser#polyParams.
    def enterPolyParams(self, ctx:OdinParser.PolyParamsContext):
        pass

    # Exit a parse tree produced by OdinParser#polyParams.
    def exitPolyParams(self, ctx:OdinParser.PolyParamsContext):
        pass


    # Enter a parse tree produced by OdinParser#polyParamList.
    def enterPolyParamList(self, ctx:OdinParser.PolyParamListContext):
        pass

    # Exit a parse tree produced by OdinParser#polyParamList.
    def exitPolyParamList(self, ctx:OdinParser.PolyParamListContext):
        pass


    # Enter a parse tree produced by OdinParser#polyParam.
    def enterPolyParam(self, ctx:OdinParser.PolyParamContext):
        pass

    # Exit a parse tree produced by OdinParser#polyParam.
    def exitPolyParam(self, ctx:OdinParser.PolyParamContext):
        pass


    # Enter a parse tree produced by OdinParser#paramList.
    def enterParamList(self, ctx:OdinParser.ParamListContext):
        pass

    # Exit a parse tree produced by OdinParser#paramList.
    def exitParamList(self, ctx:OdinParser.ParamListContext):
        pass


    # Enter a parse tree produced by OdinParser#param.
    def enterParam(self, ctx:OdinParser.ParamContext):
        pass

    # Exit a parse tree produced by OdinParser#param.
    def exitParam(self, ctx:OdinParser.ParamContext):
        pass


    # Enter a parse tree produced by OdinParser#returnTypes.
    def enterReturnTypes(self, ctx:OdinParser.ReturnTypesContext):
        pass

    # Exit a parse tree produced by OdinParser#returnTypes.
    def exitReturnTypes(self, ctx:OdinParser.ReturnTypesContext):
        pass


    # Enter a parse tree produced by OdinParser#returnFieldList.
    def enterReturnFieldList(self, ctx:OdinParser.ReturnFieldListContext):
        pass

    # Exit a parse tree produced by OdinParser#returnFieldList.
    def exitReturnFieldList(self, ctx:OdinParser.ReturnFieldListContext):
        pass


    # Enter a parse tree produced by OdinParser#returnField.
    def enterReturnField(self, ctx:OdinParser.ReturnFieldContext):
        pass

    # Exit a parse tree produced by OdinParser#returnField.
    def exitReturnField(self, ctx:OdinParser.ReturnFieldContext):
        pass


    # Enter a parse tree produced by OdinParser#procBody.
    def enterProcBody(self, ctx:OdinParser.ProcBodyContext):
        pass

    # Exit a parse tree produced by OdinParser#procBody.
    def exitProcBody(self, ctx:OdinParser.ProcBodyContext):
        pass


    # Enter a parse tree produced by OdinParser#block.
    def enterBlock(self, ctx:OdinParser.BlockContext):
        pass

    # Exit a parse tree produced by OdinParser#block.
    def exitBlock(self, ctx:OdinParser.BlockContext):
        pass


    # Enter a parse tree produced by OdinParser#stmt.
    def enterStmt(self, ctx:OdinParser.StmtContext):
        pass

    # Exit a parse tree produced by OdinParser#stmt.
    def exitStmt(self, ctx:OdinParser.StmtContext):
        pass


    # Enter a parse tree produced by OdinParser#labelStmt.
    def enterLabelStmt(self, ctx:OdinParser.LabelStmtContext):
        pass

    # Exit a parse tree produced by OdinParser#labelStmt.
    def exitLabelStmt(self, ctx:OdinParser.LabelStmtContext):
        pass


    # Enter a parse tree produced by OdinParser#directiveStmt.
    def enterDirectiveStmt(self, ctx:OdinParser.DirectiveStmtContext):
        pass

    # Exit a parse tree produced by OdinParser#directiveStmt.
    def exitDirectiveStmt(self, ctx:OdinParser.DirectiveStmtContext):
        pass


    # Enter a parse tree produced by OdinParser#returnStmt.
    def enterReturnStmt(self, ctx:OdinParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by OdinParser#returnStmt.
    def exitReturnStmt(self, ctx:OdinParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by OdinParser#deferStmt.
    def enterDeferStmt(self, ctx:OdinParser.DeferStmtContext):
        pass

    # Exit a parse tree produced by OdinParser#deferStmt.
    def exitDeferStmt(self, ctx:OdinParser.DeferStmtContext):
        pass


    # Enter a parse tree produced by OdinParser#ifStmt.
    def enterIfStmt(self, ctx:OdinParser.IfStmtContext):
        pass

    # Exit a parse tree produced by OdinParser#ifStmt.
    def exitIfStmt(self, ctx:OdinParser.IfStmtContext):
        pass


    # Enter a parse tree produced by OdinParser#whenStmt.
    def enterWhenStmt(self, ctx:OdinParser.WhenStmtContext):
        pass

    # Exit a parse tree produced by OdinParser#whenStmt.
    def exitWhenStmt(self, ctx:OdinParser.WhenStmtContext):
        pass


    # Enter a parse tree produced by OdinParser#forStmt.
    def enterForStmt(self, ctx:OdinParser.ForStmtContext):
        pass

    # Exit a parse tree produced by OdinParser#forStmt.
    def exitForStmt(self, ctx:OdinParser.ForStmtContext):
        pass


    # Enter a parse tree produced by OdinParser#forClause.
    def enterForClause(self, ctx:OdinParser.ForClauseContext):
        pass

    # Exit a parse tree produced by OdinParser#forClause.
    def exitForClause(self, ctx:OdinParser.ForClauseContext):
        pass


    # Enter a parse tree produced by OdinParser#switchStmt.
    def enterSwitchStmt(self, ctx:OdinParser.SwitchStmtContext):
        pass

    # Exit a parse tree produced by OdinParser#switchStmt.
    def exitSwitchStmt(self, ctx:OdinParser.SwitchStmtContext):
        pass


    # Enter a parse tree produced by OdinParser#switchCase.
    def enterSwitchCase(self, ctx:OdinParser.SwitchCaseContext):
        pass

    # Exit a parse tree produced by OdinParser#switchCase.
    def exitSwitchCase(self, ctx:OdinParser.SwitchCaseContext):
        pass


    # Enter a parse tree produced by OdinParser#assignStmt.
    def enterAssignStmt(self, ctx:OdinParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by OdinParser#assignStmt.
    def exitAssignStmt(self, ctx:OdinParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by OdinParser#assignOp.
    def enterAssignOp(self, ctx:OdinParser.AssignOpContext):
        pass

    # Exit a parse tree produced by OdinParser#assignOp.
    def exitAssignOp(self, ctx:OdinParser.AssignOpContext):
        pass


    # Enter a parse tree produced by OdinParser#simpleStmt.
    def enterSimpleStmt(self, ctx:OdinParser.SimpleStmtContext):
        pass

    # Exit a parse tree produced by OdinParser#simpleStmt.
    def exitSimpleStmt(self, ctx:OdinParser.SimpleStmtContext):
        pass


    # Enter a parse tree produced by OdinParser#exprStmt.
    def enterExprStmt(self, ctx:OdinParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by OdinParser#exprStmt.
    def exitExprStmt(self, ctx:OdinParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by OdinParser#type.
    def enterType(self, ctx:OdinParser.TypeContext):
        pass

    # Exit a parse tree produced by OdinParser#type.
    def exitType(self, ctx:OdinParser.TypeContext):
        pass


    # Enter a parse tree produced by OdinParser#pointerType.
    def enterPointerType(self, ctx:OdinParser.PointerTypeContext):
        pass

    # Exit a parse tree produced by OdinParser#pointerType.
    def exitPointerType(self, ctx:OdinParser.PointerTypeContext):
        pass


    # Enter a parse tree produced by OdinParser#sliceType.
    def enterSliceType(self, ctx:OdinParser.SliceTypeContext):
        pass

    # Exit a parse tree produced by OdinParser#sliceType.
    def exitSliceType(self, ctx:OdinParser.SliceTypeContext):
        pass


    # Enter a parse tree produced by OdinParser#dynArrayType.
    def enterDynArrayType(self, ctx:OdinParser.DynArrayTypeContext):
        pass

    # Exit a parse tree produced by OdinParser#dynArrayType.
    def exitDynArrayType(self, ctx:OdinParser.DynArrayTypeContext):
        pass


    # Enter a parse tree produced by OdinParser#arrayType.
    def enterArrayType(self, ctx:OdinParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by OdinParser#arrayType.
    def exitArrayType(self, ctx:OdinParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by OdinParser#mapType.
    def enterMapType(self, ctx:OdinParser.MapTypeContext):
        pass

    # Exit a parse tree produced by OdinParser#mapType.
    def exitMapType(self, ctx:OdinParser.MapTypeContext):
        pass


    # Enter a parse tree produced by OdinParser#matrixType.
    def enterMatrixType(self, ctx:OdinParser.MatrixTypeContext):
        pass

    # Exit a parse tree produced by OdinParser#matrixType.
    def exitMatrixType(self, ctx:OdinParser.MatrixTypeContext):
        pass


    # Enter a parse tree produced by OdinParser#procType.
    def enterProcType(self, ctx:OdinParser.ProcTypeContext):
        pass

    # Exit a parse tree produced by OdinParser#procType.
    def exitProcType(self, ctx:OdinParser.ProcTypeContext):
        pass


    # Enter a parse tree produced by OdinParser#distinctType.
    def enterDistinctType(self, ctx:OdinParser.DistinctTypeContext):
        pass

    # Exit a parse tree produced by OdinParser#distinctType.
    def exitDistinctType(self, ctx:OdinParser.DistinctTypeContext):
        pass


    # Enter a parse tree produced by OdinParser#polyType.
    def enterPolyType(self, ctx:OdinParser.PolyTypeContext):
        pass

    # Exit a parse tree produced by OdinParser#polyType.
    def exitPolyType(self, ctx:OdinParser.PolyTypeContext):
        pass


    # Enter a parse tree produced by OdinParser#specializedType.
    def enterSpecializedType(self, ctx:OdinParser.SpecializedTypeContext):
        pass

    # Exit a parse tree produced by OdinParser#specializedType.
    def exitSpecializedType(self, ctx:OdinParser.SpecializedTypeContext):
        pass


    # Enter a parse tree produced by OdinParser#qualifiedIdent.
    def enterQualifiedIdent(self, ctx:OdinParser.QualifiedIdentContext):
        pass

    # Exit a parse tree produced by OdinParser#qualifiedIdent.
    def exitQualifiedIdent(self, ctx:OdinParser.QualifiedIdentContext):
        pass


    # Enter a parse tree produced by OdinParser#AutoCastExpr.
    def enterAutoCastExpr(self, ctx:OdinParser.AutoCastExprContext):
        pass

    # Exit a parse tree produced by OdinParser#AutoCastExpr.
    def exitAutoCastExpr(self, ctx:OdinParser.AutoCastExprContext):
        pass


    # Enter a parse tree produced by OdinParser#DerefExpr.
    def enterDerefExpr(self, ctx:OdinParser.DerefExprContext):
        pass

    # Exit a parse tree produced by OdinParser#DerefExpr.
    def exitDerefExpr(self, ctx:OdinParser.DerefExprContext):
        pass


    # Enter a parse tree produced by OdinParser#TypeAssertExpr.
    def enterTypeAssertExpr(self, ctx:OdinParser.TypeAssertExprContext):
        pass

    # Exit a parse tree produced by OdinParser#TypeAssertExpr.
    def exitTypeAssertExpr(self, ctx:OdinParser.TypeAssertExprContext):
        pass


    # Enter a parse tree produced by OdinParser#RelationalExpr.
    def enterRelationalExpr(self, ctx:OdinParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by OdinParser#RelationalExpr.
    def exitRelationalExpr(self, ctx:OdinParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by OdinParser#IndexOrSliceExpr.
    def enterIndexOrSliceExpr(self, ctx:OdinParser.IndexOrSliceExprContext):
        pass

    # Exit a parse tree produced by OdinParser#IndexOrSliceExpr.
    def exitIndexOrSliceExpr(self, ctx:OdinParser.IndexOrSliceExprContext):
        pass


    # Enter a parse tree produced by OdinParser#LogicalAndExpr.
    def enterLogicalAndExpr(self, ctx:OdinParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by OdinParser#LogicalAndExpr.
    def exitLogicalAndExpr(self, ctx:OdinParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by OdinParser#MultiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:OdinParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by OdinParser#MultiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:OdinParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by OdinParser#TypeidExpr.
    def enterTypeidExpr(self, ctx:OdinParser.TypeidExprContext):
        pass

    # Exit a parse tree produced by OdinParser#TypeidExpr.
    def exitTypeidExpr(self, ctx:OdinParser.TypeidExprContext):
        pass


    # Enter a parse tree produced by OdinParser#IdentifierExpr.
    def enterIdentifierExpr(self, ctx:OdinParser.IdentifierExprContext):
        pass

    # Exit a parse tree produced by OdinParser#IdentifierExpr.
    def exitIdentifierExpr(self, ctx:OdinParser.IdentifierExprContext):
        pass


    # Enter a parse tree produced by OdinParser#CastExpr.
    def enterCastExpr(self, ctx:OdinParser.CastExprContext):
        pass

    # Exit a parse tree produced by OdinParser#CastExpr.
    def exitCastExpr(self, ctx:OdinParser.CastExprContext):
        pass


    # Enter a parse tree produced by OdinParser#LiteralExpr.
    def enterLiteralExpr(self, ctx:OdinParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by OdinParser#LiteralExpr.
    def exitLiteralExpr(self, ctx:OdinParser.LiteralExprContext):
        pass


    # Enter a parse tree produced by OdinParser#PolyParamExpr.
    def enterPolyParamExpr(self, ctx:OdinParser.PolyParamExprContext):
        pass

    # Exit a parse tree produced by OdinParser#PolyParamExpr.
    def exitPolyParamExpr(self, ctx:OdinParser.PolyParamExprContext):
        pass


    # Enter a parse tree produced by OdinParser#CompoundLitExpr.
    def enterCompoundLitExpr(self, ctx:OdinParser.CompoundLitExprContext):
        pass

    # Exit a parse tree produced by OdinParser#CompoundLitExpr.
    def exitCompoundLitExpr(self, ctx:OdinParser.CompoundLitExprContext):
        pass


    # Enter a parse tree produced by OdinParser#CallExpr.
    def enterCallExpr(self, ctx:OdinParser.CallExprContext):
        pass

    # Exit a parse tree produced by OdinParser#CallExpr.
    def exitCallExpr(self, ctx:OdinParser.CallExprContext):
        pass


    # Enter a parse tree produced by OdinParser#InExpr.
    def enterInExpr(self, ctx:OdinParser.InExprContext):
        pass

    # Exit a parse tree produced by OdinParser#InExpr.
    def exitInExpr(self, ctx:OdinParser.InExprContext):
        pass


    # Enter a parse tree produced by OdinParser#TernaryExpr.
    def enterTernaryExpr(self, ctx:OdinParser.TernaryExprContext):
        pass

    # Exit a parse tree produced by OdinParser#TernaryExpr.
    def exitTernaryExpr(self, ctx:OdinParser.TernaryExprContext):
        pass


    # Enter a parse tree produced by OdinParser#ImplicitSelectorExpr.
    def enterImplicitSelectorExpr(self, ctx:OdinParser.ImplicitSelectorExprContext):
        pass

    # Exit a parse tree produced by OdinParser#ImplicitSelectorExpr.
    def exitImplicitSelectorExpr(self, ctx:OdinParser.ImplicitSelectorExprContext):
        pass


    # Enter a parse tree produced by OdinParser#PostfixControlExpr.
    def enterPostfixControlExpr(self, ctx:OdinParser.PostfixControlExprContext):
        pass

    # Exit a parse tree produced by OdinParser#PostfixControlExpr.
    def exitPostfixControlExpr(self, ctx:OdinParser.PostfixControlExprContext):
        pass


    # Enter a parse tree produced by OdinParser#RangeExpr.
    def enterRangeExpr(self, ctx:OdinParser.RangeExprContext):
        pass

    # Exit a parse tree produced by OdinParser#RangeExpr.
    def exitRangeExpr(self, ctx:OdinParser.RangeExprContext):
        pass


    # Enter a parse tree produced by OdinParser#UnaryExpr.
    def enterUnaryExpr(self, ctx:OdinParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by OdinParser#UnaryExpr.
    def exitUnaryExpr(self, ctx:OdinParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by OdinParser#DirectiveExpr.
    def enterDirectiveExpr(self, ctx:OdinParser.DirectiveExprContext):
        pass

    # Exit a parse tree produced by OdinParser#DirectiveExpr.
    def exitDirectiveExpr(self, ctx:OdinParser.DirectiveExprContext):
        pass


    # Enter a parse tree produced by OdinParser#LogicalOrExpr.
    def enterLogicalOrExpr(self, ctx:OdinParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by OdinParser#LogicalOrExpr.
    def exitLogicalOrExpr(self, ctx:OdinParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by OdinParser#AdditiveExpr.
    def enterAdditiveExpr(self, ctx:OdinParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by OdinParser#AdditiveExpr.
    def exitAdditiveExpr(self, ctx:OdinParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by OdinParser#ParenExpr.
    def enterParenExpr(self, ctx:OdinParser.ParenExprContext):
        pass

    # Exit a parse tree produced by OdinParser#ParenExpr.
    def exitParenExpr(self, ctx:OdinParser.ParenExprContext):
        pass


    # Enter a parse tree produced by OdinParser#MemberAccessExpr.
    def enterMemberAccessExpr(self, ctx:OdinParser.MemberAccessExprContext):
        pass

    # Exit a parse tree produced by OdinParser#MemberAccessExpr.
    def exitMemberAccessExpr(self, ctx:OdinParser.MemberAccessExprContext):
        pass


    # Enter a parse tree produced by OdinParser#argumentList.
    def enterArgumentList(self, ctx:OdinParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by OdinParser#argumentList.
    def exitArgumentList(self, ctx:OdinParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by OdinParser#argument.
    def enterArgument(self, ctx:OdinParser.ArgumentContext):
        pass

    # Exit a parse tree produced by OdinParser#argument.
    def exitArgument(self, ctx:OdinParser.ArgumentContext):
        pass


    # Enter a parse tree produced by OdinParser#compoundLiteral.
    def enterCompoundLiteral(self, ctx:OdinParser.CompoundLiteralContext):
        pass

    # Exit a parse tree produced by OdinParser#compoundLiteral.
    def exitCompoundLiteral(self, ctx:OdinParser.CompoundLiteralContext):
        pass


    # Enter a parse tree produced by OdinParser#literal.
    def enterLiteral(self, ctx:OdinParser.LiteralContext):
        pass

    # Exit a parse tree produced by OdinParser#literal.
    def exitLiteral(self, ctx:OdinParser.LiteralContext):
        pass



del OdinParser