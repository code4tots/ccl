# Generated from java-escape by ANTLR 4.5
# encoding: utf-8
from antlr4 import *
from io import StringIO
package = globals().get("__package__", None)
ischild = len(package)>0 if package is not None else False
if ischild:
    from .CclListener import CclListener
else:
    from CclListener import CclListener
def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\23")
        buf.write("Y\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\3\2\3\2\3\3\7\3\24\n\3\f\3\16\3\27\13\3\3\4\3\4\3")
        buf.write("\4\3\5\3\5\3\5\7\5\37\n\5\f\5\16\5\"\13\5\3\5\5\5%\n\5")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\7\6/\n\6\f\6\16\6\62")
        buf.write("\13\6\3\6\5\6\65\n\6\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3")
        buf.write("\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\5\bG\n\b\3\b\3\b\3\b\3")
        buf.write("\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\7\bT\n\b\f\b\16\bW\13\b")
        buf.write("\3\b\2\3\16\t\2\4\6\b\n\f\16\2\4\3\2\f\r\3\2\16\17]\2")
        buf.write("\20\3\2\2\2\4\25\3\2\2\2\6\30\3\2\2\2\b$\3\2\2\2\n\64")
        buf.write("\3\2\2\2\f\66\3\2\2\2\16F\3\2\2\2\20\21\5\4\3\2\21\3\3")
        buf.write("\2\2\2\22\24\5\6\4\2\23\22\3\2\2\2\24\27\3\2\2\2\25\23")
        buf.write("\3\2\2\2\25\26\3\2\2\2\26\5\3\2\2\2\27\25\3\2\2\2\30\31")
        buf.write("\5\16\b\2\31\32\7\3\2\2\32\7\3\2\2\2\33 \5\16\b\2\34\35")
        buf.write("\7\4\2\2\35\37\5\16\b\2\36\34\3\2\2\2\37\"\3\2\2\2 \36")
        buf.write("\3\2\2\2 !\3\2\2\2!%\3\2\2\2\" \3\2\2\2#%\3\2\2\2$\33")
        buf.write("\3\2\2\2$#\3\2\2\2%\t\3\2\2\2&\'\5\16\b\2\'(\7\5\2\2(")
        buf.write("\60\5\16\b\2)*\7\4\2\2*+\5\16\b\2+,\7\5\2\2,-\5\16\b\2")
        buf.write("-/\3\2\2\2.)\3\2\2\2/\62\3\2\2\2\60.\3\2\2\2\60\61\3\2")
        buf.write("\2\2\61\65\3\2\2\2\62\60\3\2\2\2\63\65\3\2\2\2\64&\3\2")
        buf.write("\2\2\64\63\3\2\2\2\65\13\3\2\2\2\66\67\7\6\2\2\678\5\4")
        buf.write("\3\289\7\7\2\29\r\3\2\2\2:;\b\b\1\2;G\7\20\2\2<G\7\21")
        buf.write("\2\2=G\7\22\2\2>?\7\b\2\2?@\5\16\b\2@A\7\t\2\2AG\3\2\2")
        buf.write("\2BC\7\n\2\2CD\5\b\5\2DE\7\13\2\2EG\3\2\2\2F:\3\2\2\2")
        buf.write("F<\3\2\2\2F=\3\2\2\2F>\3\2\2\2FB\3\2\2\2GU\3\2\2\2HI\f")
        buf.write("\4\2\2IJ\t\2\2\2JT\5\16\b\5KL\f\3\2\2LM\t\3\2\2MT\5\16")
        buf.write("\b\4NO\f\5\2\2OP\7\b\2\2PQ\5\b\5\2QR\7\t\2\2RT\3\2\2\2")
        buf.write("SH\3\2\2\2SK\3\2\2\2SN\3\2\2\2TW\3\2\2\2US\3\2\2\2UV\3")
        buf.write("\2\2\2V\17\3\2\2\2WU\3\2\2\2\n\25 $\60\64FSU")
        return buf.getvalue()


class CclParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"';'", u"','", u"':'", u"'{'", u"'}'", 
                     u"'('", u"')'", u"'['", u"']'", u"'*'", u"'/'", u"'+'", 
                     u"'-'" ]

    symbolicNames = [ u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"NUM", u"STR", u"ID", 
                      u"WS" ]

    RULE_start = 0
    RULE_stmts = 1
    RULE_stmt = 2
    RULE_exprs = 3
    RULE_exprPairs = 4
    RULE_block = 5
    RULE_expr = 6

    ruleNames =  [ "start", "stmts", "stmt", "exprs", "exprPairs", "block", 
                   "expr" ]

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
    NUM=14
    STR=15
    ID=16
    WS=17

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
            return self.getTypedRuleContext(CclParser.StmtsContext,0)


        def getRuleIndex(self):
            return CclParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitStart(self)




    def start(self):

        localctx = CclParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
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
                return self.getTypedRuleContexts(CclParser.StmtContext)
            else:
                return self.getTypedRuleContext(CclParser.StmtContext,i)


        def getRuleIndex(self):
            return CclParser.RULE_stmts

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterStmts(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitStmts(self)




    def stmts(self):

        localctx = CclParser.StmtsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stmts)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CclParser.T__5) | (1 << CclParser.T__7) | (1 << CclParser.NUM) | (1 << CclParser.STR) | (1 << CclParser.ID))) != 0):
                self.state = 16
                self.stmt()
                self.state = 21
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

        def expr(self):
            return self.getTypedRuleContext(CclParser.ExprContext,0)


        def getRuleIndex(self):
            return CclParser.RULE_stmt

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitStmt(self)




    def stmt(self):

        localctx = CclParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 22
            self.expr(0)
            self.state = 23
            self.match(CclParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExprsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CclParser.ExprContext)
            else:
                return self.getTypedRuleContext(CclParser.ExprContext,i)


        def getRuleIndex(self):
            return CclParser.RULE_exprs

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterExprs(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitExprs(self)




    def exprs(self):

        localctx = CclParser.ExprsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_exprs)
        self._la = 0 # Token type
        try:
            self.state = 34
            token = self._input.LA(1)
            if token in [CclParser.T__5, CclParser.T__7, CclParser.NUM, CclParser.STR, CclParser.ID]:
                self.enterOuterAlt(localctx, 1)
                self.state = 25
                self.expr(0)
                self.state = 30
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CclParser.T__1:
                    self.state = 26
                    self.match(CclParser.T__1)
                    self.state = 27
                    self.expr(0)
                    self.state = 32
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)


            elif token in [CclParser.T__6, CclParser.T__8]:
                self.enterOuterAlt(localctx, 2)


            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExprPairsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CclParser.ExprContext)
            else:
                return self.getTypedRuleContext(CclParser.ExprContext,i)


        def getRuleIndex(self):
            return CclParser.RULE_exprPairs

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterExprPairs(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitExprPairs(self)




    def exprPairs(self):

        localctx = CclParser.ExprPairsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_exprPairs)
        self._la = 0 # Token type
        try:
            self.state = 50
            token = self._input.LA(1)
            if token in [CclParser.T__5, CclParser.T__7, CclParser.NUM, CclParser.STR, CclParser.ID]:
                self.enterOuterAlt(localctx, 1)
                self.state = 36
                self.expr(0)
                self.state = 37
                self.match(CclParser.T__2)
                self.state = 38
                self.expr(0)
                self.state = 46
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CclParser.T__1:
                    self.state = 39
                    self.match(CclParser.T__1)
                    self.state = 40
                    self.expr(0)
                    self.state = 41
                    self.match(CclParser.T__2)
                    self.state = 42
                    self.expr(0)
                    self.state = 48
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)


            elif token in [CclParser.EOF]:
                self.enterOuterAlt(localctx, 2)


            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BlockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmts(self):
            return self.getTypedRuleContext(CclParser.StmtsContext,0)


        def getRuleIndex(self):
            return CclParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitBlock(self)




    def block(self):

        localctx = CclParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_block)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self.match(CclParser.T__3)
            self.state = 53
            self.stmts()
            self.state = 54
            self.match(CclParser.T__4)
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
            return CclParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class StrExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.atom = None # Token
            self.copyFrom(ctx)

        def STR(self):
            return self.getToken(CclParser.STR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterStrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitStrExpr(self)


    class ParExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CclParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterParExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitParExpr(self)


    class BinOpExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.left = None # ExprContext
            self.op = None # Token
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CclParser.ExprContext)
            else:
                return self.getTypedRuleContext(CclParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterBinOpExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitBinOpExpr(self)


    class CallExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.fn = None # ExprContext
            self.args = None # ExprsContext
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CclParser.ExprContext,0)

        def exprs(self):
            return self.getTypedRuleContext(CclParser.ExprsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterCallExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitCallExpr(self)


    class ListExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def exprs(self):
            return self.getTypedRuleContext(CclParser.ExprsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterListExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitListExpr(self)


    class NumExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.atom = None # Token
            self.copyFrom(ctx)

        def NUM(self):
            return self.getToken(CclParser.NUM, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterNumExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitNumExpr(self)


    class IdExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.atom = None # Token
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(CclParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterIdExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitIdExpr(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CclParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 12
        self.enterRecursionRule(localctx, 12, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            token = self._input.LA(1)
            if token in [CclParser.NUM]:
                localctx = CclParser.NumExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 57
                localctx.atom = self.match(CclParser.NUM)

            elif token in [CclParser.STR]:
                localctx = CclParser.StrExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 58
                localctx.atom = self.match(CclParser.STR)

            elif token in [CclParser.ID]:
                localctx = CclParser.IdExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 59
                localctx.atom = self.match(CclParser.ID)

            elif token in [CclParser.T__5]:
                localctx = CclParser.ParExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 60
                self.match(CclParser.T__5)
                self.state = 61
                self.expr(0)
                self.state = 62
                self.match(CclParser.T__6)

            elif token in [CclParser.T__7]:
                localctx = CclParser.ListExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 64
                self.match(CclParser.T__7)
                self.state = 65
                self.exprs()
                self.state = 66
                self.match(CclParser.T__8)

            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 83
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 81
                    la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
                    if la_ == 1:
                        localctx = CclParser.BinOpExprContext(self, CclParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 70
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 71
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==CclParser.T__9 or _la==CclParser.T__10):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self.consume()
                        self.state = 72
                        localctx.right = self.expr(3)
                        pass

                    elif la_ == 2:
                        localctx = CclParser.BinOpExprContext(self, CclParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 73
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 74
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==CclParser.T__11 or _la==CclParser.T__12):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self.consume()
                        self.state = 75
                        localctx.right = self.expr(2)
                        pass

                    elif la_ == 3:
                        localctx = CclParser.CallExprContext(self, CclParser.ExprContext(self, _parentctx, _parentState))
                        localctx.fn = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 76
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 77
                        self.match(CclParser.T__5)
                        self.state = 78
                        localctx.args = self.exprs()
                        self.state = 79
                        self.match(CclParser.T__6)
                        pass

             
                self.state = 85
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[6] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 3)
         



