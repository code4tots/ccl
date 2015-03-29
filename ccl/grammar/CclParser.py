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
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\f")
        buf.write("\60\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\3\2\3\2\3\2\3\3\7")
        buf.write("\3\17\n\3\f\3\16\3\22\13\3\3\4\3\4\3\4\3\5\3\5\3\5\3\5")
        buf.write("\3\5\5\5\34\n\5\3\5\3\5\3\5\3\5\3\5\7\5#\n\5\f\5\16\5")
        buf.write("&\13\5\5\5(\n\5\3\5\7\5+\n\5\f\5\16\5.\13\5\3\5\2\3\b")
        buf.write("\6\2\4\6\b\2\2\62\2\n\3\2\2\2\4\20\3\2\2\2\6\23\3\2\2")
        buf.write("\2\b\33\3\2\2\2\n\13\5\4\3\2\13\f\7\2\2\3\f\3\3\2\2\2")
        buf.write("\r\17\5\6\4\2\16\r\3\2\2\2\17\22\3\2\2\2\20\16\3\2\2\2")
        buf.write("\20\21\3\2\2\2\21\5\3\2\2\2\22\20\3\2\2\2\23\24\5\b\5")
        buf.write("\2\24\25\7\3\2\2\25\7\3\2\2\2\26\27\b\5\1\2\27\34\7\t")
        buf.write("\2\2\30\34\7\7\2\2\31\34\7\b\2\2\32\34\7\n\2\2\33\26\3")
        buf.write("\2\2\2\33\30\3\2\2\2\33\31\3\2\2\2\33\32\3\2\2\2\34,\3")
        buf.write("\2\2\2\35\36\f\3\2\2\36\'\7\4\2\2\37$\5\b\5\2 !\7\5\2")
        buf.write("\2!#\5\b\5\2\" \3\2\2\2#&\3\2\2\2$\"\3\2\2\2$%\3\2\2\2")
        buf.write("%(\3\2\2\2&$\3\2\2\2\'\37\3\2\2\2\'(\3\2\2\2()\3\2\2\2")
        buf.write(")+\7\6\2\2*\35\3\2\2\2+.\3\2\2\2,*\3\2\2\2,-\3\2\2\2-")
        buf.write("\t\3\2\2\2.,\3\2\2\2\7\20\33$\',")
        return buf.getvalue()


class CclParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"';'", u"'('", u"','", u"')'" ]

    symbolicNames = [ u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"FLOAT", u"INT", u"STR", u"NAME", u"CMT", 
                      u"WS" ]

    RULE_start = 0
    RULE_ss = 1
    RULE_s = 2
    RULE_e = 3

    ruleNames =  [ "start", "ss", "s", "e" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    FLOAT=5
    INT=6
    STR=7
    NAME=8
    CMT=9
    WS=10

    def __init__(self, input:TokenStream):
        super().__init__(input)
        self.checkVersion("4.5")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class StartContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ss(self):
            return self.getTypedRuleContext(CclParser.SsContext,0)


        def EOF(self):
            return self.getToken(CclParser.EOF, 0)

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
            self.state = 8
            self.ss()
            self.state = 9
            self.match(CclParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def s(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CclParser.SContext)
            else:
                return self.getTypedRuleContext(CclParser.SContext,i)


        def getRuleIndex(self):
            return CclParser.RULE_ss

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterSs(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitSs(self)




    def ss(self):

        localctx = CclParser.SsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_ss)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CclParser.FLOAT) | (1 << CclParser.INT) | (1 << CclParser.STR) | (1 << CclParser.NAME))) != 0):
                self.state = 11
                self.s()
                self.state = 16
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class SContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CclParser.RULE_s

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ExpressionContext(SContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.SContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def e(self):
            return self.getTypedRuleContext(CclParser.EContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitExpression(self)



    def s(self):

        localctx = CclParser.SContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_s)
        try:
            localctx = CclParser.ExpressionContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self.e(0)
            self.state = 18
            self.match(CclParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CclParser.RULE_e

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class StrContext(EContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.EContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def STR(self):
            return self.getToken(CclParser.STR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterStr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitStr(self)


    class CallContext(EContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.EContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def e(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CclParser.EContext)
            else:
                return self.getTypedRuleContext(CclParser.EContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitCall(self)


    class NameContext(EContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.EContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def NAME(self):
            return self.getToken(CclParser.NAME, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterName(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitName(self)


    class FloatContext(EContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.EContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def FLOAT(self):
            return self.getToken(CclParser.FLOAT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterFloat(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitFloat(self)


    class IntContext(EContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.EContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(CclParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterInt(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitInt(self)



    def e(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CclParser.EContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_e, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 25
            token = self._input.LA(1)
            if token in [CclParser.STR]:
                localctx = CclParser.StrContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 21
                self.match(CclParser.STR)

            elif token in [CclParser.FLOAT]:
                localctx = CclParser.FloatContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 22
                self.match(CclParser.FLOAT)

            elif token in [CclParser.INT]:
                localctx = CclParser.IntContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 23
                self.match(CclParser.INT)

            elif token in [CclParser.NAME]:
                localctx = CclParser.NameContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 24
                self.match(CclParser.NAME)

            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 42
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = CclParser.CallContext(self, CclParser.EContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_e)
                    self.state = 27
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 28
                    self.match(CclParser.T__1)
                    self.state = 37
                    _la = self._input.LA(1)
                    if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CclParser.FLOAT) | (1 << CclParser.INT) | (1 << CclParser.STR) | (1 << CclParser.NAME))) != 0):
                        self.state = 29
                        self.e(0)
                        self.state = 34
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while _la==CclParser.T__2:
                            self.state = 30
                            self.match(CclParser.T__2)
                            self.state = 31
                            self.e(0)
                            self.state = 36
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)



                    self.state = 39
                    self.match(CclParser.T__3) 
                self.state = 44
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
        self._predicates[3] = self.e_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def e_sempred(self, localctx:EContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         



