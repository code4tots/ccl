# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from antlr4 import *
from io import StringIO
package = globals().get("__package__", None)
ischild = len(package)>0 if package is not None else False
if ischild:
    from .BubListener import BubListener
else:
    from BubListener import BubListener
def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\25")
        buf.write("a\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2\3\3")
        buf.write("\7\3\20\n\3\f\3\16\3\23\13\3\3\4\3\4\3\4\3\4\5\4\31\n")
        buf.write("\4\3\5\6\5\34\n\5\r\5\16\5\35\3\5\3\5\3\5\3\5\3\5\3\5")
        buf.write("\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3")
        buf.write("\5\3\5\3\5\3\5\3\5\5\58\n\5\3\6\3\6\3\6\3\6\3\6\7\6?\n")
        buf.write("\6\f\6\16\6B\13\6\3\6\3\6\3\6\3\6\3\6\3\6\7\6J\n\6\f\6")
        buf.write("\16\6M\13\6\3\6\3\6\3\6\3\6\3\6\3\6\7\6U\n\6\f\6\16\6")
        buf.write("X\13\6\3\6\3\6\3\6\3\6\3\6\5\6_\n\6\3\6\2\2\7\2\4\6\b")
        buf.write("\n\2\2m\2\f\3\2\2\2\4\21\3\2\2\2\6\30\3\2\2\2\b\67\3\2")
        buf.write("\2\2\n^\3\2\2\2\f\r\5\4\3\2\r\3\3\2\2\2\16\20\5\6\4\2")
        buf.write("\17\16\3\2\2\2\20\23\3\2\2\2\21\17\3\2\2\2\21\22\3\2\2")
        buf.write("\2\22\5\3\2\2\2\23\21\3\2\2\2\24\25\5\b\5\2\25\26\7\20")
        buf.write("\2\2\26\31\3\2\2\2\27\31\7\20\2\2\30\24\3\2\2\2\30\27")
        buf.write("\3\2\2\2\31\7\3\2\2\2\32\34\5\n\6\2\33\32\3\2\2\2\34\35")
        buf.write("\3\2\2\2\35\33\3\2\2\2\35\36\3\2\2\2\368\3\2\2\2\37 \7")
        buf.write("\3\2\2 !\5\4\3\2!\"\7\4\2\2\"8\3\2\2\2#$\7\5\2\2$%\5\n")
        buf.write("\6\2%&\5\6\4\2&\'\7\6\2\2\'(\5\6\4\2(8\3\2\2\2)*\7\5\2")
        buf.write("\2*+\5\n\6\2+,\5\6\4\2,8\3\2\2\2-.\7\7\2\2./\5\n\6\2/")
        buf.write("\60\5\6\4\2\608\3\2\2\2\61\62\7\23\2\2\62\63\7\b\2\2\63")
        buf.write("8\5\n\6\2\64\65\7\23\2\2\65\66\7\t\2\2\668\5\n\6\2\67")
        buf.write("\33\3\2\2\2\67\37\3\2\2\2\67#\3\2\2\2\67)\3\2\2\2\67-")
        buf.write("\3\2\2\2\67\61\3\2\2\2\67\64\3\2\2\28\t\3\2\2\29_\7\21")
        buf.write("\2\2:_\7\22\2\2;_\7\23\2\2<@\7\n\2\2=?\7\23\2\2>=\3\2")
        buf.write("\2\2?B\3\2\2\2@>\3\2\2\2@A\3\2\2\2AC\3\2\2\2B@\3\2\2\2")
        buf.write("CD\7\3\2\2DE\5\4\3\2EF\7\4\2\2F_\3\2\2\2GK\7\13\2\2HJ")
        buf.write("\5\n\6\2IH\3\2\2\2JM\3\2\2\2KI\3\2\2\2KL\3\2\2\2LN\3\2")
        buf.write("\2\2MK\3\2\2\2N_\7\f\2\2OV\7\13\2\2PQ\5\n\6\2QR\7\r\2")
        buf.write("\2RS\5\n\6\2SU\3\2\2\2TP\3\2\2\2UX\3\2\2\2VT\3\2\2\2V")
        buf.write("W\3\2\2\2WY\3\2\2\2XV\3\2\2\2Y_\7\f\2\2Z[\7\16\2\2[\\")
        buf.write("\5\b\5\2\\]\7\17\2\2]_\3\2\2\2^9\3\2\2\2^:\3\2\2\2^;\3")
        buf.write("\2\2\2^<\3\2\2\2^G\3\2\2\2^O\3\2\2\2^Z\3\2\2\2_\13\3\2")
        buf.write("\2\2\n\21\30\35\67@KV^")
        return buf.getvalue()


class BubParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'{'", u"'}'", u"'if'", u"'else'", u"'while'", 
                     u"':='", u"'='", u"'\\'", u"'['", u"']'", u"':'", u"'('", 
                     u"')'" ]

    symbolicNames = [ u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"DELIM", u"NUM", u"STR", 
                      u"ID", u"CMT", u"WS" ]

    RULE_start = 0
    RULE_stmts = 1
    RULE_stmt = 2
    RULE_cmd = 3
    RULE_expr = 4

    ruleNames =  [ "start", "stmts", "stmt", "cmd", "expr" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    DELIM=14
    NUM=15
    STR=16
    ID=17
    CMT=18
    WS=19

    def __init__(self, input:TokenStream):
        super().__init__(input)
        self.checkVersion("4.5")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class StartContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmts(self):
            return self.getTypedRuleContext(BubParser.StmtsContext,0)


        def getRuleIndex(self):
            return BubParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitStart(self)




    def start(self):

        localctx = BubParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self.stmts()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StmtsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BubParser.StmtContext)
            else:
                return self.getTypedRuleContext(BubParser.StmtContext,i)


        def getRuleIndex(self):
            return BubParser.RULE_stmts

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterStmts(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitStmts(self)




    def stmts(self):

        localctx = BubParser.StmtsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stmts)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << BubParser.T__0) | (1 << BubParser.T__2) | (1 << BubParser.T__4) | (1 << BubParser.T__7) | (1 << BubParser.T__8) | (1 << BubParser.T__11) | (1 << BubParser.DELIM) | (1 << BubParser.NUM) | (1 << BubParser.STR) | (1 << BubParser.ID))) != 0):
                self.state = 12
                self.stmt()
                self.state = 17
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StmtContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def cmd(self):
            return self.getTypedRuleContext(BubParser.CmdContext,0)


        def DELIM(self):
            return self.getToken(BubParser.DELIM, 0)

        def getRuleIndex(self):
            return BubParser.RULE_stmt

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitStmt(self)




    def stmt(self):

        localctx = BubParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_stmt)
        try:
            self.state = 22
            token = self._input.LA(1)
            if token in [BubParser.T__0, BubParser.T__2, BubParser.T__4, BubParser.T__7, BubParser.T__8, BubParser.T__11, BubParser.NUM, BubParser.STR, BubParser.ID]:
                self.enterOuterAlt(localctx, 1)
                self.state = 18
                self.cmd()
                self.state = 19
                self.match(BubParser.DELIM)

            elif token in [BubParser.DELIM]:
                self.enterOuterAlt(localctx, 2)
                self.state = 21
                self.match(BubParser.DELIM)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CmdContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return BubParser.RULE_cmd

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class CallContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BubParser.ExprContext)
            else:
                return self.getTypedRuleContext(BubParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitCall(self)


    class AssignmentContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(BubParser.ID, 0)
        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitAssignment(self)


    class BlockContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def stmts(self):
            return self.getTypedRuleContext(BubParser.StmtsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitBlock(self)


    class WhileContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)

        def stmt(self):
            return self.getTypedRuleContext(BubParser.StmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterWhile(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitWhile(self)


    class IfElseContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BubParser.StmtContext)
            else:
                return self.getTypedRuleContext(BubParser.StmtContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterIfElse(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitIfElse(self)


    class IfContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)

        def stmt(self):
            return self.getTypedRuleContext(BubParser.StmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterIf(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitIf(self)


    class DeclarationContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(BubParser.ID, 0)
        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitDeclaration(self)



    def cmd(self):

        localctx = BubParser.CmdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_cmd)
        self._la = 0 # Token type
        try:
            self.state = 53
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = BubParser.CallContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 25 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 24
                    self.expr()
                    self.state = 27 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << BubParser.T__7) | (1 << BubParser.T__8) | (1 << BubParser.T__11) | (1 << BubParser.NUM) | (1 << BubParser.STR) | (1 << BubParser.ID))) != 0)):
                        break

                pass

            elif la_ == 2:
                localctx = BubParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 29
                self.match(BubParser.T__0)
                self.state = 30
                self.stmts()
                self.state = 31
                self.match(BubParser.T__1)
                pass

            elif la_ == 3:
                localctx = BubParser.IfElseContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 33
                self.match(BubParser.T__2)
                self.state = 34
                self.expr()
                self.state = 35
                self.stmt()
                self.state = 36
                self.match(BubParser.T__3)
                self.state = 37
                self.stmt()
                pass

            elif la_ == 4:
                localctx = BubParser.IfContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 39
                self.match(BubParser.T__2)
                self.state = 40
                self.expr()
                self.state = 41
                self.stmt()
                pass

            elif la_ == 5:
                localctx = BubParser.WhileContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 43
                self.match(BubParser.T__4)
                self.state = 44
                self.expr()
                self.state = 45
                self.stmt()
                pass

            elif la_ == 6:
                localctx = BubParser.DeclarationContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 47
                self.match(BubParser.ID)
                self.state = 48
                self.match(BubParser.T__5)
                self.state = 49
                self.expr()
                pass

            elif la_ == 7:
                localctx = BubParser.AssignmentContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 50
                self.match(BubParser.ID)
                self.state = 51
                self.match(BubParser.T__6)
                self.state = 52
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return BubParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class StrContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def STR(self):
            return self.getToken(BubParser.STR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterStr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitStr(self)


    class LambdaContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def stmts(self):
            return self.getTypedRuleContext(BubParser.StmtsContext,0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(BubParser.ID)
            else:
                return self.getToken(BubParser.ID, i)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterLambda(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitLambda(self)


    class CmdExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def cmd(self):
            return self.getTypedRuleContext(BubParser.CmdContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterCmdExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitCmdExpr(self)


    class NumContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUM(self):
            return self.getToken(BubParser.NUM, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterNum(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitNum(self)


    class DictContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BubParser.ExprContext)
            else:
                return self.getTypedRuleContext(BubParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterDict(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitDict(self)


    class IdContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(BubParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterId(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitId(self)


    class ListContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BubParser.ExprContext)
            else:
                return self.getTypedRuleContext(BubParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterList(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitList(self)



    def expr(self):

        localctx = BubParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.state = 92
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                localctx = BubParser.NumContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 55
                self.match(BubParser.NUM)
                pass

            elif la_ == 2:
                localctx = BubParser.StrContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 56
                self.match(BubParser.STR)
                pass

            elif la_ == 3:
                localctx = BubParser.IdContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 57
                self.match(BubParser.ID)
                pass

            elif la_ == 4:
                localctx = BubParser.LambdaContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 58
                self.match(BubParser.T__7)
                self.state = 62
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==BubParser.ID:
                    self.state = 59
                    self.match(BubParser.ID)
                    self.state = 64
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 65
                self.match(BubParser.T__0)
                self.state = 66
                self.stmts()
                self.state = 67
                self.match(BubParser.T__1)
                pass

            elif la_ == 5:
                localctx = BubParser.ListContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 69
                self.match(BubParser.T__8)
                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << BubParser.T__7) | (1 << BubParser.T__8) | (1 << BubParser.T__11) | (1 << BubParser.NUM) | (1 << BubParser.STR) | (1 << BubParser.ID))) != 0):
                    self.state = 70
                    self.expr()
                    self.state = 75
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 76
                self.match(BubParser.T__9)
                pass

            elif la_ == 6:
                localctx = BubParser.DictContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 77
                self.match(BubParser.T__8)
                self.state = 84
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << BubParser.T__7) | (1 << BubParser.T__8) | (1 << BubParser.T__11) | (1 << BubParser.NUM) | (1 << BubParser.STR) | (1 << BubParser.ID))) != 0):
                    self.state = 78
                    self.expr()
                    self.state = 79
                    self.match(BubParser.T__10)
                    self.state = 80
                    self.expr()
                    self.state = 86
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 87
                self.match(BubParser.T__9)
                pass

            elif la_ == 7:
                localctx = BubParser.CmdExprContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 88
                self.match(BubParser.T__11)
                self.state = 89
                self.cmd()
                self.state = 90
                self.match(BubParser.T__12)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx




