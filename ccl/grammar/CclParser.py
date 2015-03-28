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
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\24")
        buf.write("\\\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\3\2\3\2\3\2\3\3\5\3")
        buf.write("\17\n\3\3\3\7\3\22\n\3\f\3\16\3\25\13\3\3\4\6\4\30\n\4")
        buf.write("\r\4\16\4\31\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3")
        buf.write("\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\5\4\64\n\4\3\5\3\5\3\5\3\5\7\5:\n\5\f\5\16\5=\13\5\3")
        buf.write("\5\3\5\3\5\3\5\3\5\3\5\7\5E\n\5\f\5\16\5H\13\5\3\5\3\5")
        buf.write("\3\5\3\5\3\5\3\5\7\5P\n\5\f\5\16\5S\13\5\3\5\3\5\3\5\3")
        buf.write("\5\3\5\5\5Z\n\5\3\5\2\2\6\2\4\6\b\2\2h\2\n\3\2\2\2\4\23")
        buf.write("\3\2\2\2\6\63\3\2\2\2\bY\3\2\2\2\n\13\5\4\3\2\13\f\7\2")
        buf.write("\2\3\f\3\3\2\2\2\r\17\5\6\4\2\16\r\3\2\2\2\16\17\3\2\2")
        buf.write("\2\17\20\3\2\2\2\20\22\7\20\2\2\21\16\3\2\2\2\22\25\3")
        buf.write("\2\2\2\23\21\3\2\2\2\23\24\3\2\2\2\24\5\3\2\2\2\25\23")
        buf.write("\3\2\2\2\26\30\5\b\5\2\27\26\3\2\2\2\30\31\3\2\2\2\31")
        buf.write("\27\3\2\2\2\31\32\3\2\2\2\32\64\3\2\2\2\33\34\7\3\2\2")
        buf.write("\34\35\5\4\3\2\35\36\7\4\2\2\36\64\3\2\2\2\37 \7\5\2\2")
        buf.write(" !\5\b\5\2!\"\5\6\4\2\"#\7\6\2\2#$\5\6\4\2$\64\3\2\2\2")
        buf.write("%&\7\5\2\2&\'\5\b\5\2\'(\5\6\4\2(\64\3\2\2\2)*\7\7\2\2")
        buf.write("*+\5\b\5\2+,\5\6\4\2,\64\3\2\2\2-.\7\21\2\2./\7\b\2\2")
        buf.write("/\64\5\b\5\2\60\61\7\21\2\2\61\62\7\t\2\2\62\64\5\b\5")
        buf.write("\2\63\27\3\2\2\2\63\33\3\2\2\2\63\37\3\2\2\2\63%\3\2\2")
        buf.write("\2\63)\3\2\2\2\63-\3\2\2\2\63\60\3\2\2\2\64\7\3\2\2\2")
        buf.write("\65Z\7\21\2\2\66Z\7\22\2\2\67;\7\n\2\28:\7\21\2\298\3")
        buf.write("\2\2\2:=\3\2\2\2;9\3\2\2\2;<\3\2\2\2<>\3\2\2\2=;\3\2\2")
        buf.write("\2>?\7\3\2\2?@\5\4\3\2@A\7\4\2\2AZ\3\2\2\2BF\7\13\2\2")
        buf.write("CE\5\b\5\2DC\3\2\2\2EH\3\2\2\2FD\3\2\2\2FG\3\2\2\2GI\3")
        buf.write("\2\2\2HF\3\2\2\2IZ\7\f\2\2JQ\7\13\2\2KL\5\b\5\2LM\7\r")
        buf.write("\2\2MN\5\b\5\2NP\3\2\2\2OK\3\2\2\2PS\3\2\2\2QO\3\2\2\2")
        buf.write("QR\3\2\2\2RT\3\2\2\2SQ\3\2\2\2TZ\7\f\2\2UV\7\16\2\2VW")
        buf.write("\5\6\4\2WX\7\17\2\2XZ\3\2\2\2Y\65\3\2\2\2Y\66\3\2\2\2")
        buf.write("Y\67\3\2\2\2YB\3\2\2\2YJ\3\2\2\2YU\3\2\2\2Z\t\3\2\2\2")
        buf.write("\n\16\23\31\63;FQY")
        return buf.getvalue()


class CclParser ( Parser ):

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
                      u"<INVALID>", u"<INVALID>", u"DELIM", u"STR", u"VAR", 
                      u"CMT", u"WS" ]

    RULE_start = 0
    RULE_stmts = 1
    RULE_stmt = 2
    RULE_expr = 3

    ruleNames =  [ "start", "stmts", "stmt", "expr" ]

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
    STR=15
    VAR=16
    CMT=17
    WS=18

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
            self.stmts()
            self.state = 9
            self.match(CclParser.EOF)
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

        def DELIM(self, i:int=None):
            if i is None:
                return self.getTokens(CclParser.DELIM)
            else:
                return self.getToken(CclParser.DELIM, i)

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
            self.state = 17
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CclParser.T__0) | (1 << CclParser.T__2) | (1 << CclParser.T__4) | (1 << CclParser.T__7) | (1 << CclParser.T__8) | (1 << CclParser.T__11) | (1 << CclParser.DELIM) | (1 << CclParser.STR) | (1 << CclParser.VAR))) != 0):
                self.state = 12
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CclParser.T__0) | (1 << CclParser.T__2) | (1 << CclParser.T__4) | (1 << CclParser.T__7) | (1 << CclParser.T__8) | (1 << CclParser.T__11) | (1 << CclParser.STR) | (1 << CclParser.VAR))) != 0):
                    self.state = 11
                    self.stmt()


                self.state = 14
                self.match(CclParser.DELIM)
                self.state = 19
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


        def getRuleIndex(self):
            return CclParser.RULE_stmt

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class CallContext(StmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.StmtContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CclParser.ExprContext)
            else:
                return self.getTypedRuleContext(CclParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitCall(self)


    class DeclContext(StmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.StmtContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def STR(self):
            return self.getToken(CclParser.STR, 0)
        def expr(self):
            return self.getTypedRuleContext(CclParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitDecl(self)


    class BlockContext(StmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.StmtContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def stmts(self):
            return self.getTypedRuleContext(CclParser.StmtsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitBlock(self)


    class WhileContext(StmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.StmtContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CclParser.ExprContext,0)

        def stmt(self):
            return self.getTypedRuleContext(CclParser.StmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterWhile(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitWhile(self)


    class IfElseContext(StmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.StmtContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CclParser.ExprContext,0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CclParser.StmtContext)
            else:
                return self.getTypedRuleContext(CclParser.StmtContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterIfElse(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitIfElse(self)


    class IfContext(StmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.StmtContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(CclParser.ExprContext,0)

        def stmt(self):
            return self.getTypedRuleContext(CclParser.StmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterIf(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitIf(self)


    class AssignContext(StmtContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.StmtContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def STR(self):
            return self.getToken(CclParser.STR, 0)
        def expr(self):
            return self.getTypedRuleContext(CclParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterAssign(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitAssign(self)



    def stmt(self):

        localctx = CclParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_stmt)
        self._la = 0 # Token type
        try:
            self.state = 49
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = CclParser.CallContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 21 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 20
                    self.expr()
                    self.state = 23 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CclParser.T__7) | (1 << CclParser.T__8) | (1 << CclParser.T__11) | (1 << CclParser.STR) | (1 << CclParser.VAR))) != 0)):
                        break

                pass

            elif la_ == 2:
                localctx = CclParser.BlockContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 25
                self.match(CclParser.T__0)
                self.state = 26
                self.stmts()
                self.state = 27
                self.match(CclParser.T__1)
                pass

            elif la_ == 3:
                localctx = CclParser.IfElseContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 29
                self.match(CclParser.T__2)
                self.state = 30
                self.expr()
                self.state = 31
                self.stmt()
                self.state = 32
                self.match(CclParser.T__3)
                self.state = 33
                self.stmt()
                pass

            elif la_ == 4:
                localctx = CclParser.IfContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 35
                self.match(CclParser.T__2)
                self.state = 36
                self.expr()
                self.state = 37
                self.stmt()
                pass

            elif la_ == 5:
                localctx = CclParser.WhileContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 39
                self.match(CclParser.T__4)
                self.state = 40
                self.expr()
                self.state = 41
                self.stmt()
                pass

            elif la_ == 6:
                localctx = CclParser.DeclContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 43
                self.match(CclParser.STR)
                self.state = 44
                self.match(CclParser.T__5)
                self.state = 45
                self.expr()
                pass

            elif la_ == 7:
                localctx = CclParser.AssignContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 46
                self.match(CclParser.STR)
                self.state = 47
                self.match(CclParser.T__6)
                self.state = 48
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
            return CclParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class StrContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
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


    class LambdaContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def stmts(self):
            return self.getTypedRuleContext(CclParser.StmtsContext,0)

        def STR(self, i:int=None):
            if i is None:
                return self.getTokens(CclParser.STR)
            else:
                return self.getToken(CclParser.STR, i)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterLambda(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitLambda(self)


    class VarContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def VAR(self):
            return self.getToken(CclParser.VAR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterVar(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitVar(self)


    class DictContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CclParser.ExprContext)
            else:
                return self.getTypedRuleContext(CclParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterDict(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitDict(self)


    class CmdContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def stmt(self):
            return self.getTypedRuleContext(CclParser.StmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterCmd(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitCmd(self)


    class ListContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CclParser.ExprContext)
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CclParser.ExprContext)
            else:
                return self.getTypedRuleContext(CclParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.enterList(self)

        def exitRule(self, listener:ParseTreeListener):
            if isinstance( listener, CclListener ):
                listener.exitList(self)



    def expr(self):

        localctx = CclParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.state = 87
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                localctx = CclParser.StrContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 51
                self.match(CclParser.STR)
                pass

            elif la_ == 2:
                localctx = CclParser.VarContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 52
                self.match(CclParser.VAR)
                pass

            elif la_ == 3:
                localctx = CclParser.LambdaContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 53
                self.match(CclParser.T__7)
                self.state = 57
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==CclParser.STR:
                    self.state = 54
                    self.match(CclParser.STR)
                    self.state = 59
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 60
                self.match(CclParser.T__0)
                self.state = 61
                self.stmts()
                self.state = 62
                self.match(CclParser.T__1)
                pass

            elif la_ == 4:
                localctx = CclParser.ListContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 64
                self.match(CclParser.T__8)
                self.state = 68
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CclParser.T__7) | (1 << CclParser.T__8) | (1 << CclParser.T__11) | (1 << CclParser.STR) | (1 << CclParser.VAR))) != 0):
                    self.state = 65
                    self.expr()
                    self.state = 70
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 71
                self.match(CclParser.T__9)
                pass

            elif la_ == 5:
                localctx = CclParser.DictContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 72
                self.match(CclParser.T__8)
                self.state = 79
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CclParser.T__7) | (1 << CclParser.T__8) | (1 << CclParser.T__11) | (1 << CclParser.STR) | (1 << CclParser.VAR))) != 0):
                    self.state = 73
                    self.expr()
                    self.state = 74
                    self.match(CclParser.T__10)
                    self.state = 75
                    self.expr()
                    self.state = 81
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 82
                self.match(CclParser.T__9)
                pass

            elif la_ == 6:
                localctx = CclParser.CmdContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 83
                self.match(CclParser.T__11)
                self.state = 84
                self.stmt()
                self.state = 85
                self.match(CclParser.T__12)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx




