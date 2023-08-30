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
	javac -d bin *.java

mqtt:
	python cmd_sender.py

setup:
	scp -r ../cmd gaofeng@10.10.170.171:~/zhouweixian/script-server/scripts