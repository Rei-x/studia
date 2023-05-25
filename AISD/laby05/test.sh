javac -d ./dist/ Main.java
cd dist
java Main <../input.txt >../testOutput.txt
cd ..
diff testOutput.txt output.txt
