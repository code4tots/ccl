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
        buf.write("K\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\3\2\3\2\3\3\7\3\26\n\3\f\3\16\3\31\13\3\3")
        buf.write("\4\3\4\3\4\3\4\3\4\5\4 \n\4\3\5\3\5\3\5\3\5\3\5\3\5\3")
        buf.write("\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\3\5\5\5\63\n\5")
        buf.write("\3\6\3\6\3\6\3\6\3\6\3\6\3\6\5\6<\n\6\3\7\3\7\7\7@\n\7")
        buf.write("\f\7\16\7C\13\7\3\b\3\b\3\t\3\t\3\t\3\t\3\t\2\2\n\2\4")
        buf.write("\6\b\n\f\16\20\2\3\3\3\3\4N\2\22\3\2\2\2\4\27\3\2\2\2")
        buf.write("\6\37\3\2\2\2\b\62\3\2\2\2\n;\3\2\2\2\fA\3\2\2\2\16D\3")
        buf.write("\2\2\2\20F\3\2\2\2\22\23\5\4\3\2\23\3\3\2\2\2\24\26\5")
        buf.write("\6\4\2\25\24\3\2\2\2\26\31\3\2\2\2\27\25\3\2\2\2\27\30")
        buf.write("\3\2\2\2\30\5\3\2\2\2\31\27\3\2\2\2\32\33\5\b\5\2\33\34")
        buf.write("\t\2\2\2\34 \3\2\2\2\35 \7\3\2\2\36 \7\4\2\2\37\32\3\2")
        buf.write("\2\2\37\35\3\2\2\2\37\36\3\2\2\2 \7\3\2\2\2!\"\5\n\6\2")
        buf.write("\"#\5\f\7\2#\63\3\2\2\2$%\7\5\2\2%&\5\n\6\2&\'\5\b\5\2")
        buf.write("\'\63\3\2\2\2()\7\6\2\2)*\5\4\3\2*+\7\7\2\2+\63\3\2\2")
        buf.write("\2,-\7\16\2\2-.\7\b\2\2.\63\5\n\6\2/\60\7\16\2\2\60\61")
        buf.write("\7\t\2\2\61\63\5\n\6\2\62!\3\2\2\2\62$\3\2\2\2\62(\3\2")
        buf.write("\2\2\62,\3\2\2\2\62/\3\2\2\2\63\t\3\2\2\2\64<\7\f\2\2")
        buf.write("\65<\7\r\2\2\66<\7\16\2\2\678\7\n\2\289\5\b\5\29:\7\13")
        buf.write("\2\2:<\3\2\2\2;\64\3\2\2\2;\65\3\2\2\2;\66\3\2\2\2;\67")
        buf.write("\3\2\2\2<\13\3\2\2\2=@\5\16\b\2>@\5\20\t\2?=\3\2\2\2?")
        buf.write(">\3\2\2\2@C\3\2\2\2A?\3\2\2\2AB\3\2\2\2B\r\3\2\2\2CA\3")
        buf.write("\2\2\2DE\5\n\6\2E\17\3\2\2\2FG\7\16\2\2GH\7\t\2\2HI\5")
        buf.write("\n\6\2I\21\3\2\2\2\b\27\37\62;?A")
        return buf.getvalue()


class BubParser ( Parser ):

    grammarFileName = "java-escape"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ u"<INVALID>", u"'\n'", u"';'", u"'while'", u"'{'", 
                     u"'}'", u"':='", u"'='", u"'('", u"')'" ]

    symbolicNames = [ u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"<INVALID>", u"<INVALID>", 
                      u"<INVALID>", u"<INVALID>", u"NUM", u"STR", u"ID", 
                      u"CMT", u"WS" ]

    RULE_start = 0
    RULE_stmts = 1
    RULE_stmt = 2
    RULE_cmd = 3
    RULE_expr = 4
    RULE_args = 5
    RULE_arg = 6
    RULE_kwarg = 7

    ruleNames =  [ "start", "stmts", "stmt", "cmd", "expr", "args", "arg", 
                   "kwarg" ]

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
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << BubParser.T__0) | (1 << BubParser.T__1) | (1 << BubParser.T__2) | (1 << BubParser.T__3) | (1 << BubParser.T__7) | (1 << BubParser.NUM) | (1 << BubParser.STR) | (1 << BubParser.ID))) != 0):
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
            if token in [BubParser.T__2, BubParser.T__3, BubParser.T__7, BubParser.NUM, BubParser.STR, BubParser.ID]:
                self.enterOuterAlt(localctx, 1)
                self.state = 24
                self.cmd()
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

        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)

        def args(self):
            return self.getTypedRuleContext(BubParser.ArgsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitCall(self)


    class AssignmentContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.name = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)

        def ID(self):
            return self.getToken(BubParser.ID, 0)

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

        def cmd(self):
            return self.getTypedRuleContext(BubParser.CmdContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterWhile(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitWhile(self)


    class DeclarationContext(CmdContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.CmdContext)
            super().__init__(parser)
            self.name = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)

        def ID(self):
            return self.getToken(BubParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitDeclaration(self)



    def cmd(self):

        localctx = BubParser.CmdContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_cmd)
        try:
            self.state = 48
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = BubParser.CallContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 31
                self.expr()
                self.state = 32
                self.args()
                pass

            elif la_ == 2:
                localctx = BubParser.WhileContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 34
                self.match(BubParser.T__2)
                self.state = 35
                self.expr()
                self.state = 36
                self.cmd()
                pass

            elif la_ == 3:
                localctx = BubParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 38
                self.match(BubParser.T__3)
                self.state = 39
                self.stmts()
                self.state = 40
                self.match(BubParser.T__4)
                pass

            elif la_ == 4:
                localctx = BubParser.DeclarationContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 42
                localctx.name = self.match(BubParser.ID)
                self.state = 43
                self.match(BubParser.T__5)
                self.state = 44
                self.expr()
                pass

            elif la_ == 5:
                localctx = BubParser.AssignmentContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 45
                localctx.name = self.match(BubParser.ID)
                self.state = 46
                self.match(BubParser.T__6)
                self.state = 47
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
            self.atom = None # Token
            self.copyFrom(ctx)

        def STR(self):
            return self.getToken(BubParser.STR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterStr(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitStr(self)


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
            self.atom = None # Token
            self.copyFrom(ctx)

        def NUM(self):
            return self.getToken(BubParser.NUM, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterNum(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitNum(self)


    class IdContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a BubParser.ExprContext)
            super().__init__(parser)
            self.atom = None # Token
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(BubParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.enterId(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, BubListener ):
                listener.exitId(self)



    def expr(self):

        localctx = BubParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_expr)
        try:
            self.state = 57
            token = self._input.LA(1)
            if token in [BubParser.NUM]:
                localctx = BubParser.NumContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 50
                localctx.atom = self.match(BubParser.NUM)

            elif token in [BubParser.STR]:
                localctx = BubParser.StrContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 51
                localctx.atom = self.match(BubParser.STR)

            elif token in [BubParser.ID]:
                localctx = BubParser.IdContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 52
                localctx.atom = self.match(BubParser.ID)

            elif token in [BubParser.T__7]:
                localctx = BubParser.CmdExprContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 53
                self.match(BubParser.T__7)
                self.state = 54
                self.cmd()
                self.state = 55
                self.match(BubParser.T__8)

            else:
                raise NoViableAltException(self)

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
        self.enterRule(localctx, 10, self.RULE_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << BubParser.T__7) | (1 << BubParser.NUM) | (1 << BubParser.STR) | (1 << BubParser.ID))) != 0):
                self.state = 61
                la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                if la_ == 1:
                    self.state = 59
                    self.arg()
                    pass

                elif la_ == 2:
                    self.state = 60
                    self.kwarg()
                    pass


                self.state = 65
                self._errHandler.sync(self)
                _la = self._input.LA(1)

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
        self.enterRule(localctx, 12, self.RULE_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
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
            self.name = None # Token

        def expr(self):
            return self.getTypedRuleContext(BubParser.ExprContext,0)


        def ID(self):
            return self.getToken(BubParser.ID, 0)

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
        self.enterRule(localctx, 14, self.RULE_kwarg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            localctx.name = self.match(BubParser.ID)
            self.state = 69
            self.match(BubParser.T__6)
            self.state = 70
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx




