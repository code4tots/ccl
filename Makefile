.PHONY: clean runjavahw

runandroid: BaseAaProgram.java AndroidAaProgram.java
	echo "package com.example.math4tots.template;" > Template/app/src/main/java/com/example/math4tots/template/BaseAaProgram.java
	cat BaseAaProgram.java >> Template/app/src/main/java/com/example/math4tots/template/BaseAaProgram.java
	echo "package com.example.math4tots.template;" > Template/app/src/main/java/com/example/math4tots/template/AndroidAaProgram.java
	cat AndroidAaProgram.java >> Template/app/src/main/java/com/example/math4tots/template/AndroidAaProgram.java
	cd Template && ./gradlew assembleDebug && ./gradlew installDebug

runjavahw: BaseAaProgram.class HwAaProgram.class
	java HwAaProgram

Aa.tokens AaLexer.tokens AaLexer.py AaListener.py AaParser.py: Aa.g4
	# alias antlr4
	java -jar /usr/local/lib/antlr-4.5-complete.jar -Dlanguage=Python3 Aa.g4

HwAaProgram.java: hw.aa AaLexer.py AaListener.py AaParser.py aa.py
	cat hw.aa | python3 aa.py java HwAaProgram BaseAaProgram > HwAaProgram.java

AndroidAaProgram.java: android.aa AaLexer.py AaListener.py AaParser.py aa.py
	cat android.aa | python3 aa.py java AndroidAaProgram BaseAaProgram > AndroidAaProgram.java

BaseAaProgram.class HwAaProgram.class AndroidAaProgram.class: BaseAaProgram.java HwAaProgram.java AndroidAaProgram.java
	javac *.java

clean:
	rm -rf \
		__pycache__ *.pyc *.class \
		Aa.tokens AaLexer.tokens AaLexer.py AaListener.py AaParser.py \
		HwAaProgram.java
