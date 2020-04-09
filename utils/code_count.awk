
#!/bin/awk
BEGIN{authorname="null"}
{
  if($1=="Author:"){
    authorname=$2;
  }
  if($2=="insertions(+)"||$5=="insertions(+),"){
    author[authorname]+=$4;
  }
}END{
  for(a in author){
    print(a,author[a]);
  }
}
