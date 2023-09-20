:PHONY clean build test

clean: 
	-rm *.pyc
	-rm *.zip
	-rm -rf build
	-rm -rf *.egg-info

sub:
	-../../secret/remove_sensitive.sh . sub
res:
	-../../secret/remove_sensitive.sh . res

javac:
	javac -d bin src/*.java

jar:
	cd bin && jar -cvfm aes.jar ./MANIFEST.MF *

runj:
	java -cp ./bin src.Aes 'hello world' 'mysecretkey' encrypt
	java -cp ./bin src.Aes 'cGFyYW1zdHIu7Wf85ouqQfJae1HEh8Lv36xwAiLJEPsRKBDP6fPEONMFacAVG+d0' 'mysecretkey' decrypt
	java -jar ./bin/aes.jar 'hello world' 'mysecretkey' encrypt
	java -jar ./bin/aes.jar 'cGFyYW1zdHI+vogaGldj0+n3pV7BxgKNKTyv15cLPdI=' 'mysecretkey' decrypt

mqtt:
	python cmd_sender.py

setup:
	scp -r ../cmd gaofeng@10.10.170.209:~/zhouweixian/script-server/scripts