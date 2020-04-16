from dico import *
from get_sym import *
results=[]
def do_exit():
	for match in matches:
				print("=================================================")

				print(match[0]+" with probability "+str(match[2]))
				print("Reasons:")
				for x in match[1]:
					if(x[2]==1):
						print(x[0])
				print("=================================================")
	exit()
def sort(listp):
	flag=0
	l=len(listp)
	for i in range(0,l):
		for j in range(0,l-i-1):
			if(listp[j][2]<listp[j+1][2]):
				flag=1
				temp=listp[j]
				listp[j]=listp[j+1]
				listp[j+1]=temp
	return(listp,flag)
def probabz():
	#print("yes")
	zsum=0
	for m in range(0,len(matches)):
		matches[m][2]=0
		for i in range(0,len(matches[m][1])):
			if(matches[m][1][i][2]==1):
				matches[m][2]=matches[m][2]+matches[m][1][i][1]
		zsum=zsum+matches[m][2]
	for i in range(0,len(matches)):
		matches[i][2]=matches[i][2]/zsum
	return(matches)

def update_matches(x,matches):
	for i in range(0,len(matches)):
		for k in range(0,len(matches[i][1])):
			if(matches[i][1][k][0]==x):
				matches[i][1][k][2]=1
	return(probabz())

def find_match(v):
	sum=0
	for disease in diseases:
		flag=0
		disease.append(0)
		for x in v:
			for i in range(0,len(disease[1])):
				if(disease[1][i][0]==x):
					disease[1][i][2]=1
					disease[2]=disease[2]+disease[1][i][1]
					flag=1
		if(flag==1):
			results.append(disease)
		sum=sum+disease[2]
	return(results,sum)

#@app.route("/initiale",methods=["POST"]):
sym=input("Enter your symptoms\n") #get input from frontend
process1=txt_process(sym)
print("P1",process1)
process2=process1

sympton1=get_symps(process2)
print("s1",sympton1)
symton2=merge2s(sympton1)
print("s2",symton2)
symton3=merge3s(symton2)
print("s3",symton3)
v = clean(symton3)
print("v",v)
matches,sum=find_match(v)
#print("matches",matches)
#print("sum",sum)
for match in matches:
	match[2]=match[2]/sum
	#print(match)
ok,flag=sort(matches)
max_prob=0
count=0
packman=[]
while(count<len(matches)):
	flag=0
	print("ok",ok[count][1])
	for j in range(0,len(ok[count][1])):
		if(ok[count][1][j][2]==0 and (ok[count][1][j][0] not in packman)):
			packman.append(ok[count][1][j][0])
			if(ok[0][2]>0.5):
					print(ok[0][2])
					do_exit()
			ans=input("Do you have "+ok[count][1][j][0]+"?")
			#return (But return will exit the loop)
			for x in ok:
				print(x[0]+"  "+str(x[2]))
			print("\n")
			if(ans=="yes"):
				ok=update_matches(ok[count][1][j][0],ok)
				ok,flag=sort(ok)
				if(ok[0][2]>0.5):
					print(ok[0][2])
					do_exit()
				#print(ok)
				if(flag==1):
					break

	if(flag!=1):
		flag=0
		count=count+1
do_exit()
