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
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\r")
        buf.write("8\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2\3\3")
        buf.write("\7\3\20\n\3\f\3\16\3\23\13\3\3\4\3\4\3\4\3\5\3\5\3\5\7")
        buf.write("\5\33\n\5\f\5\16\5\36\13\5\3\6\3\6\3\6\5\6#\n\6\3\6\3")
        buf.write("\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\3\6\7\6")
        buf.write("\63\n\6\f\6\16\6\66\13\6\3\6\2\3\n\7\2\4\6\b\n\2\4\3\2")
        buf.write("\7\b\3\2\t\n9\2\f\3\2\2\2\4\21\3\2\2\2\6\24\3\2\2\2\b")
        buf.write("\27\3\2\2\2\n\"\3\2\2\2\f\r\5\4\3\2\r\3\3\2\2\2\16\20")
        buf.write("\5\6\4\2\17\16\3\2\2\2\20\23\3\2\2\2\21\17\3\2\2\2\21")
        buf.write("\22\3\2\2\2\22\5\3\2\2\2\23\21\3\2\2\2\24\25\5\n\6\2\25")
        buf.write("\26\7\3\2\2\26\7\3\2\2\2\27\34\5\n\6\2\30\31\7\4\2\2\31")
        buf.write("\33\5\n\6\2\32\30\3\2\2\2\33\36\3\2\2\2\34\32\3\2\2\2")
        buf.write("\34\35\3\2\2\2\35\t\3\2\2\2\36\34\3\2\2\2\37 \b\6\1\2")
        buf.write(" #\7\13\2\2!#\7\f\2\2\"\37\3\2\2\2\"!\3\2\2\2#\64\3\2")
        buf.write("\2\2$%\f\4\2\2%&\t\2\2\2&\63\5\n\6\5\'(\f\3\2\2()\t\3")
        buf.write("\2\2)\63\5\n\6\4*+\f\6\2\2+,\7\5\2\2,\63\7\6\2\2-.\f\5")
        buf.write("\2\2./\7\5\2\2/\60\5\b\5\2\60\61\7\6\2\2\61\63\3\2\2\2")
        buf.write("\62$\3\2\2\2\62\'\3\2\2\2\62*\3\2\2\2\62-\3\2\2\2\63\66")
        buf.write("\3\2\2\2\64\62\3\2\2\2\64\65\3\2\2\2\65\13\3\2\2\2\66")
        buf.write("\64\3\2\2\2\7\21\34\"\62\64")
        return buf.getvalue()


class CclParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"';'", u"','", u"'('", u"')'", u"'*'", 
                     u"'/'", u"'+'", u"'-'" ]

    symbolicNames = [ u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"INT", u"ID", u"WS" ]

    RULE_start = 0
    RULE_stmts = 1
    RULE_stmt = 2
    RULE_exprs = 3
    RULE_expr = 4

    ruleNames =  [ "start", "stmts", "stmt", "exprs", "expr" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    INT=9
    ID=10
    WS=11

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
            self.state = 15
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CclParser.INT or _la==CclParser.ID:
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
            self.state = 18
            self.expr(0)
            self.state = 19
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
            self.enterOuterAlt(localctx, 1)
            self.state = 21
            self.expr(0)
            self.state = 26
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CclParser.T__1:
                self.state = 22
                self.match(CclParser.T__1)
                self.state = 23
                self.expr(0)
                self.state = 28
                self._errHandler.sync(self)
                _la = self._input.LA(1)

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


    class IntExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.atom = None # Token
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(CclParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterIntExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitIntExpr(self)


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
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            token = self._input.LA(1)
            if token in [CclParser.INT]:
                localctx = CclParser.IntExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 30
                localctx.atom = self.match(CclParser.INT)

            elif token in [CclParser.ID]:
                localctx = CclParser.IdExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 31
                localctx.atom = self.match(CclParser.ID)

            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 50
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 48
                    la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                    if la_ == 1:
                        localctx = CclParser.BinOpExprContext(self, CclParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 34
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 35
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==CclParser.T__4 or _la==CclParser.T__5):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self.consume()
                        self.state = 36
                        localctx.right = self.expr(3)
                        pass

                    elif la_ == 2:
                        localctx = CclParser.BinOpExprContext(self, CclParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 37
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 38
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==CclParser.T__6 or _la==CclParser.T__7):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self.consume()
                        self.state = 39
                        localctx.right = self.expr(2)
                        pass

                    elif la_ == 3:
                        localctx = CclParser.CallExprContext(self, CclParser.ExprContext(self, _parentctx, _parentState))
                        localctx.fn = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 40
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 41
                        self.match(CclParser.T__2)
                        self.state = 42
                        self.match(CclParser.T__3)
                        pass

                    elif la_ == 4:
                        localctx = CclParser.CallExprContext(self, CclParser.ExprContext(self, _parentctx, _parentState))
                        localctx.fn = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 43
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 44
                        self.match(CclParser.T__2)
                        self.state = 45
                        localctx.args = self.exprs()
                        self.state = 46
                        self.match(CclParser.T__3)
                        pass

             
                self.state = 52
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

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
        self._predicates[4] = self.expr_sempred
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
                return self.precpred(self._ctx, 4)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 3)
         



