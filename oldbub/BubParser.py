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
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\20")
        buf.write("P\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\3\2\3\2\3\3\7\3\26\n\3\f\3\16\3\31\13\3\3")
        buf.write("\4\3\4\3\4\3\4\3\4\5\4 \n\4\3\5\3\5\3\5\3\5\3\5\3\5\3")
        buf.write("\5\5\5)\n\5\3\6\3\6\3\7\3\7\3\7\3\7\3\b\3\b\7\b\63\n\b")
        buf.write("\f\b\16\b\66\13\b\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t")
        buf.write("\3\t\3\t\3\t\3\t\3\t\5\tF\n\t\3\t\3\t\3\t\7\tK\n\t\f\t")
        buf.write("\16\tN\13\t\3\t\2\3\20\n\2\4\6\b\n\f\16\20\2\3\3\3\3\4")
        buf.write("S\2\22\3\2\2\2\4\27\3\2\2\2\6\37\3\2\2\2\b(\3\2\2\2\n")
        buf.write("*\3\2\2\2\f,\3\2\2\2\16\64\3\2\2\2\20E\3\2\2\2\22\23\5")
        buf.write("\4\3\2\23\3\3\2\2\2\24\26\5\6\4\2\25\24\3\2\2\2\26\31")
        buf.write("\3\2\2\2\27\25\3\2\2\2\27\30\3\2\2\2\30\5\3\2\2\2\31\27")
        buf.write("\3\2\2\2\32\33\5\20\t\2\33\34\t\2\2\2\34 \3\2\2\2\35 ")
        buf.write("\7\3\2\2\36 \7\4\2\2\37\32\3\2\2\2\37\35\3\2\2\2\37\36")
        buf.write("\3\2\2\2 \7\3\2\2\2!)\7\f\2\2\")\7\r\2\2#)\7\16\2\2$%")
        buf.write("\7\5\2\2%&\5\20\t\2&\'\7\6\2\2\')\3\2\2\2(!\3\2\2\2(\"")
        buf.write("\3\2\2\2(#\3\2\2\2($\3\2\2\2)\t\3\2\2\2*+\5\b\5\2+\13")
        buf.write("\3\2\2\2,-\7\16\2\2-.\7\7\2\2./\5\b\5\2/\r\3\2\2\2\60")
        buf.write("\63\5\n\6\2\61\63\5\f\7\2\62\60\3\2\2\2\62\61\3\2\2\2")
        buf.write("\63\66\3\2\2\2\64\62\3\2\2\2\64\65\3\2\2\2\65\17\3\2\2")
        buf.write("\2\66\64\3\2\2\2\678\b\t\1\289\7\16\2\29:\7\13\2\2:F\5")
        buf.write("\20\t\4;<\7\16\2\2<=\7\7\2\2=F\5\20\t\3>?\5\b\5\2?@\5")
        buf.write("\16\b\2@F\3\2\2\2AB\7\b\2\2BC\5\4\3\2CD\7\t\2\2DF\3\2")
        buf.write("\2\2E\67\3\2\2\2E;\3\2\2\2E>\3\2\2\2EA\3\2\2\2FL\3\2\2")
        buf.write("\2GH\f\5\2\2HI\7\n\2\2IK\5\b\5\2JG\3\2\2\2KN\3\2\2\2L")
        buf.write("J\3\2\2\2LM\3\2\2\2M\21\3\2\2\2NL\3\2\2\2\t\27\37(\62")
        buf.write("\64EL")
        return buf.getvalue()


class BubParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'\n'", u"';'", u"'('", u"')'", u"'='", 
                     u"'{'", u"'}'", u"'>'", u"':='" ]

    symbolicNames = [ u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"NUM", u"STR", u"ID", 
                      u"CMT", u"WS" ]

    RULE_start = 0
    RULE_stmts = 1
    RULE_stmt = 2
    RULE_expr = 3
    RULE_arg = 4
    RULE_kwarg = 5
    RULE_args = 6
    RULE_cmd = 7

    ruleNames =  [ "start", "stmts", "stmt", "expr", "arg", "kwarg", "args", 
                   "cmd" ]

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
    NUM=10
    STR=11
    ID=12
    CMT=13
    WS=14

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
            self.state = 16
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
            self.state = 21
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << BubParser.T__0) | (1 << BubParser.T__1) | (1 << BubParser.T__2) | (1 << BubParser.T__5) | (1 << BubParser.NUM) | (1 << BubParser.STR) | (1 << BubParser.ID))) != 0):
                self.state = 18
                self.stmt()
                self.state = 23
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


        def EOF(self):
            return self.getToken(BubParser.EOF, 0)

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
        self._la = 0 # Token type
        try:
            self.state = 29
            token = self._input.LA(1)
            if token in [BubParser.T__2, BubParser.T__5, BubParser.NUM, BubParser.STR, BubParser.ID]:
                self.enterOuterAlt(localctx, 1)
                self.state = 24
                self.cmd(0)
                self.state = 25
                _la = self._input.LA(1)
                if not(((((_la - -1)) & ~0x3f) == 0 and ((1 << (_la - -1)) & ((1 << (BubParser.EOF - -1)) | (1 << (BubParser.T__0 - -1)) | (1 << (BubParser.T__1 - -1)))) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self.consume()

            elif token in [BubParser.T__0]:
                self.enterOuterAlt(localctx, 2)
                self.state = 27
                self.match(BubParser.T__0)

            elif token in [BubParser.T__1]:
                self.enterOuterAlt(localctx, 3)
                self.state = 28
                self.match(BubParser.T__1)

            else:
                raise NoViableAltException(self)

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



    class StrExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.ExprContext)
            super().__init__(parser)
            self.atom = None # Token
            self.copyFrom(ctx)

        def STR(self):
            return self.getToken(BubParser.STR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterStrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitStrExpr(self)


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


    class NumExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.ExprContext)
            super().__init__(parser)
            self.atom = None # Token
            self.copyFrom(ctx)

        def NUM(self):
            return self.getToken(BubParser.NUM, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterNumExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitNumExpr(self)


    class IdExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.ExprContext)
            super().__init__(parser)
            self.atom = None # Token
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(BubParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterIdExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitIdExpr(self)



    def expr(self):

        localctx = BubParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_expr)
        try:
            self.state = 38
            token = self._input.LA(1)
            if token in [BubParser.NUM]:
                localctx = BubParser.NumExprContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 31
                localctx.atom = self.match(BubParser.NUM)

            elif token in [BubParser.STR]:
                localctx = BubParser.StrExprContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 32
                localctx.atom = self.match(BubParser.STR)

            elif token in [BubParser.ID]:
                localctx = BubParser.IdExprContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 33
                localctx.atom = self.match(BubParser.ID)

            elif token in [BubParser.T__2]:
                localctx = BubParser.CmdExprContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 34
                self.match(BubParser.T__2)
                self.state = 35
                self.cmd(0)
                self.state = 36
                self.match(BubParser.T__3)

            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArgContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)


        def getRuleIndex(self):
            return BubParser.RULE_arg

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterArg(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitArg(self)




    def arg(self):

        localctx = BubParser.ArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class KwargContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(BubParser.ID, 0)

        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)


        def getRuleIndex(self):
            return BubParser.RULE_kwarg

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterKwarg(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitKwarg(self)




    def kwarg(self):

        localctx = BubParser.KwargContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_kwarg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self.match(BubParser.ID)
            self.state = 43
            self.match(BubParser.T__4)
            self.state = 44
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArgsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BubParser.ArgContext)
            else:
                return self.getTypedRuleContext(BubParser.ArgContext,i)


        def kwarg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(BubParser.KwargContext)
            else:
                return self.getTypedRuleContext(BubParser.KwargContext,i)


        def getRuleIndex(self):
            return BubParser.RULE_args

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterArgs(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitArgs(self)




    def args(self):

        localctx = BubParser.ArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_args)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 48
                    la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                    if la_ == 1:
                        self.state = 46
                        self.arg()
                        pass

                    elif la_ == 2:
                        self.state = 47
                        self.kwarg()
                        pass

             
                self.state = 52
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

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


    class DeclareCmdContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.name = None # Token
            self.value = None # CmdContext
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(BubParser.ID, 0)
        def cmd(self):
            return self.getTypedRuleContext(BubParser.CmdContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterDeclareCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitDeclareCmd(self)


    class AssignCmdContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.name = None # Token
            self.value = None # CmdContext
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(BubParser.ID, 0)
        def cmd(self):
            return self.getTypedRuleContext(BubParser.CmdContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterAssignCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitAssignCmd(self)


    class BasicCmdContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)

        def args(self):
            return self.getTypedRuleContext(BubParser.ArgsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterBasicCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitBasicCmd(self)


    class RedirectCmdContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def cmd(self):
            return self.getTypedRuleContext(BubParser.CmdContext,0)

        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterRedirectCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitRedirectCmd(self)


    class BlockCmdContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def stmts(self):
            return self.getTypedRuleContext(BubParser.StmtsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterBlockCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitBlockCmd(self)



    def cmd(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = BubParser.CmdContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 14
        self.enterRecursionRule(localctx, 14, self.RULE_cmd, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                localctx = BubParser.DeclareCmdContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 54
                localctx.name = self.match(BubParser.ID)
                self.state = 55
                self.match(BubParser.T__8)
                self.state = 56
                localctx.value = self.cmd(2)
                pass

            elif la_ == 2:
                localctx = BubParser.AssignCmdContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 57
                localctx.name = self.match(BubParser.ID)
                self.state = 58
                self.match(BubParser.T__4)
                self.state = 59
                localctx.value = self.cmd(1)
                pass

            elif la_ == 3:
                localctx = BubParser.BasicCmdContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 60
                self.expr()
                self.state = 61
                self.args()
                pass

            elif la_ == 4:
                localctx = BubParser.BlockCmdContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 63
                self.match(BubParser.T__5)
                self.state = 64
                self.stmts()
                self.state = 65
                self.match(BubParser.T__6)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 74
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = BubParser.RedirectCmdContext(self, BubParser.CmdContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_cmd)
                    self.state = 69
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 70
                    self.match(BubParser.T__7)
                    self.state = 71
                    self.expr() 
                self.state = 76
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

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
        self._predicates[7] = self.cmd_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def cmd_sempred(self, localctx:CmdContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         



